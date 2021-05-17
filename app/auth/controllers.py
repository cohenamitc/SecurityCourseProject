import os
from uuid import uuid4
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4
import hashlib
# Import the database object from the main app module
from app import db

# Import Sendgrid Mail Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Import module forms
from app.auth.forms import LoginForm, ChangePasswordForm, SignUpForm, ForgotPassword, ResetPasswordForm

# Import module models (i.e. User)
from app.auth.models import User, History, ResetPassword, FailedLogin

# Import PassLib
from app.password_lib.passwd import PasswordLib
from app.config_service.config_service import ConfigService

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    if current_user.is_active:
        flash('Already logged in', 'info')
        return redirect(url_for('index.home'))
    # If sign in form is submitted
    form = LoginForm(request.form)
    # Verify the sign in form
    if form.validate_on_submit():
        # Original SQL Alchemy method
        # user = User.query.filter_by(email=form.email.data).first()

        # Vulnerable SQL query
        user = db.engine.execute("SELECT * FROM auth_user WHERE email='%s'" % form.email.data).first()

        # Safe SQL query
        # user = db.engine.execute("SELECT * FROM auth_user WHERE email=?", form.email.data).first()

        if user and PasswordLib().check_password(form.password.data, user.password):
            max_logins = ConfigService().get_password('failed_logins')
            last_failed = FailedLogin.query.filter_by(userid=user.id).all()
            if len(last_failed) >= max_logins:
                flash('Max failed logins exceeded, please contact admin', 'error')
                return redirect(url_for('index.home'))
            user = User.query.filter_by(id=user.id).first()
            remember = True if request.form.get('remember') else False
            login_user(user, remember)
            flash('Welcome %s' % user.name)
            delete_failed_login_records = FailedLogin.__table__.delete().where(FailedLogin.userid == user.id)
            db.session.execute(delete_failed_login_records)
            db.session.commit()
            return redirect(url_for('index.home'))
        if user:
            max_logins = ConfigService().get_password('failed_logins')
            last_failed = FailedLogin.query.filter_by(userid=user.id).all()
            if len(last_failed) >= max_logins:
                flash('Max failed logins exceeded, please contact admin', 'error')
                return redirect(url_for('index.home'))
            f = FailedLogin(userid=user.id)
            db.session.add(f)
            db.session.commit()
        flash('Wrong email or password', 'error')
    return render_template("auth/signin.html", form=form)


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_active:
        flash('Already logged in', 'info')
        return redirect(url_for('index.home'))
    # If sign in form is submitted
    form = SignUpForm(request.form)
    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user and form.password.data == form.password_confirm.data:
            # SQL_I Safe Code
            new_user = User(
                email=form.email.data,
                password=PasswordLib().get_hashed_password(form.password.data),
                name=form.name.data,
                company=form.company.data
            )
            # Original SQL Alchemy function
            # db.session.add(new_user)

            # SQL_I Vulnerable Code
            # db.engine.execute(
            #     "INSERT INTO auth_user (id, date_created, date_modified, name, email, password, status, company)\
            #      VALUES ('%s', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '%s', '%s', '%s', %d, '%s')"
            #     % (new_user.id, new_user.name, new_user.email, new_user.password, 1, new_user.company)
            # )

            # SQL_I Protected Using Parameters
            db.engine.execute(
                "INSERT INTO auth_user (id, date_created, date_modified, name, email, password, status, company)\
                VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, 1, ?)",
                new_user.id, new_user.name, new_user.email, new_user.password, new_user.company
            )

            password_history = History(
                userid=new_user.id,
                password=new_user.password
            )
            db.session.add(password_history)
            db.session.commit()
            flash(f'Welcome {form.name.data}! user created successfully', 'info')
            return redirect(url_for('index.home'))
        if form.password.data != form.password_confirm.data:
            flash('Password don\'t match!', 'error')
        else:
            flash('User already exists!', 'error')
    return render_template("auth/signup.html", form=form)


@auth.route('/signout/')
@login_required
def signout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('index.home'))


@auth.route('/changepass/', methods=['GET', 'POST'])
def change_password():
    # If sign in form is submitted
    form = ChangePasswordForm(request.form)
    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and PasswordLib().check_password(form.password.data, user.password):
            password_history_count = ConfigService().get_password('history')
            passwords = History.query.filter_by(userid=user.id).limit(password_history_count)
            for password in passwords:
                if PasswordLib().check_password(form.new_pass.data, password.password):
                    flash('Password found in near history', 'error')
                    return redirect(url_for('auth.change_password'))
            new_password_salted = PasswordLib().get_hashed_password(form.new_pass.data)
            user.password = new_password_salted
            password_history = History(
                userid=user.id,
                password=new_password_salted
            )
            db.session.add(password_history)
            db.session.commit()
            flash(f'Password changed for {user.name}!', 'info')
            return redirect(url_for('index.home'))
        flash('Wrong email or password', 'error')
    return render_template("auth/changepass.html", form=form)


@auth.route('/forgot/', methods=["GET", "POST"])
def forgot():
    if current_user.is_active:
        flash('Already logged in', 'info')
        return redirect(url_for('index.home'))
    form = ForgotPassword(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            random_hash = hashlib.sha1(str(uuid4()).encode('utf-8')).hexdigest()
            reset_record = ResetPassword(
                userid=user.id,
                random_hash=random_hash
            )
            message = Mail(
                from_email='Papa5murf@protonmail.com',
                to_emails=user.email,
                subject='Reset your password on Communication LTD',
                html_content=f'<a href="{os.environ["APP_BASE_URI"]}auth/reset/{random_hash}">{os.environ["APP_BASE_URI"]}auth/reset/{random_hash}</a>')
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(f'Sendgrid status code: {response.status_code}, reset key: {random_hash}')
            except Exception as e:
                print(e.message)
            db.session.add(reset_record)
            db.session.commit()
        flash(f'Check reset password instructions at {form.email.data}')
    return render_template('auth/forgot.html', form=form)


@auth.route('/reset/<key>', methods=["GET", "POST"])
def reset_password(key):
    if current_user.is_active:
        flash('Already logged in', 'info')
        return redirect(url_for('index.home'))
    reset_record = ResetPassword.query.filter_by(random_hash=key).first()
    if reset_record:
        user = User.query.filter_by(id=reset_record.userid).first()
        if user:
            form = ResetPasswordForm(request.form)
            if form.validate_on_submit():
                password_history_count = ConfigService().get_password('history')
                passwords = History.query.filter_by(userid=user.id).limit(password_history_count)
                for password in passwords:
                    if PasswordLib().check_password(form.password.data, password.password):
                        flash('Password found in near history', 'error')
                        return redirect(url_for('auth.change_password'))
                hashed_password = PasswordLib().get_hashed_password(form.password.data)
                user.password = hashed_password
                history = History(
                    userid=user.id,
                    password=hashed_password
                )
                db.session.add(history)
                db.session.commit()
                # Delete older records
                delete_reset_records = ResetPassword.__table__.delete().where(ResetPassword.userid == user.id)
                db.session.execute(delete_reset_records)
                db.session.commit()
                flash('Password reset successfully')
                return redirect(url_for('auth.signin'))
            return render_template('auth/reset.html', form=form, key=key)
        flash('User not found', 'error')
        return redirect(url_for('auth.signin'))
    return redirect(url_for('auth.signin'))

