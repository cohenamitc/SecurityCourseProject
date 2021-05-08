# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import login_user, logout_user, login_required

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.auth.forms import LoginForm, ChangePasswordForm, SignUpForm

# Import module models (i.e. User)
from app.auth.models import User, History

# Import PassLib
from app.password_lib.passwd import PasswordLib

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    # If sign in form is submitted
    form = LoginForm(request.form)
    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and PasswordLib().check_password(form.password.data, user.password):
            remember = True if request.form.get('remember') else False
            login_user(user, remember)
            flash('Welcome %s' % user.name)
            return redirect(url_for('index.home'))
        flash('Wrong email or password', 'error')
    return render_template("auth/signin.html", form=form)


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    # If sign in form is submitted
    form = SignUpForm(request.form)
    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user and form.password.data == form.password_confirm.data:
            new_user = User(
                email=form.email.data,
                password=PasswordLib().get_hashed_password(form.password.data),
                name=form.name.data,
                company=form.company.data
            )
            password_history = History(
                userid=new_user.id,
                password=new_user.password
            )
            db.session.add(new_user)
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
