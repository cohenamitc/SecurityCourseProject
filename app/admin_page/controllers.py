# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import login_required, current_user
# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
from app.admin_page.forms import CreateCustomer
from app.customers.models import Customer
from app.admin_page.models import Admin

# Define the blueprint: 'auth', set its url prefix: app.url/auth
admin_page = Blueprint('admin_page', __name__, url_prefix='/admin')


# Set the route and accepted methods
@admin_page.route('/', methods=["GET", "POST"])
@login_required
def manager():
    admin = Admin.query.filter_by(user_id=current_user.id).first()
    if not admin:
        flash('Not authorized!', 'error')
        return redirect(url_for('index.home'))
    new_customer_form = CreateCustomer(request.form)
    if new_customer_form.validate_on_submit():
        customer = Customer.query.filter_by(name=new_customer_form.name.data).first()
        if customer:
            flash(f'Customer {new_customer_form.name.data} already exists', 'error')
            return redirect(url_for('admin_page.manager'))
        customer = Customer(
            name=new_customer_form.name.data,
            contact=new_customer_form.contact.data,
            phone=new_customer_form.phone.data
        )
        db.session.add(customer)
        db.session.commit()
        flash(f'Customer {customer.name} created', 'info')
    return render_template("manager/manager.html", customer_form=new_customer_form)
