# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import login_required
# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
from app.customers.forms import SearchCustomer

from app.customers.models import Customer

# Define the blueprint: 'auth', set its url prefix: app.url/auth
comm_customers = Blueprint('customers', __name__, url_prefix='/customers')


# Set the route and accepted methods
@comm_customers.route('/', methods=["GET", "POST"])
@login_required
def customers():
    form = SearchCustomer(request.form)
    if form.validate_on_submit():
        customers_list = Customer.query.filter_by(name=form.name.data).all()
        if customers_list:
            return render_template("customers/customers.html", customers=customers_list, form=form)
        flash(f'Customer {form.name.data} not found', 'error')
    customers_list = Customer.query.order_by(Customer.name).all()
    return render_template("customers/customers.html", customers=customers_list, form=form)
