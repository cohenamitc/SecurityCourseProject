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
from app.sec_lib.sec_lib import SecLib

# Define the blueprint: 'auth', set its url prefix: app.url/auth
comm_customers = Blueprint('customers', __name__, url_prefix='/customers')


# Set the route and accepted methods
@comm_customers.route('/', methods=["GET", "POST"])
@login_required
def customers():
    form = SearchCustomer(request.form)
    if form.validate_on_submit():
        # Built in query from SQL Alchemy
        # customers_list = Customer.query.filter_by(name=form.name.data).all()

        # Vulnerable SQL Query
        customers_list = db.engine.execute(f"SELECT * FROM customers WHERE name='{form.name.data}'").all()

        # Safe query using parameters
        # customers_list = db.engine.execute("SELECT * FROM customers WHERE name=?", form.name.data).all()

        if customers_list:
            encoded_customers_list = []
            for customer in customers_list:
                encoded_customer = Customer(
                        name=SecLib().prevent_xss_encoding(customer.name),
                        contact=SecLib().prevent_xss_encoding(customer.contact),
                        phone=SecLib().prevent_xss_encoding(customer.phone)
                    )
                encoded_customer.date_created = customer.date_created
                encoded_customer.date_modified = customer.date_modified
                encoded_customers_list.append(
                    encoded_customer
                )
            return render_template("customers/customers.html", customers=encoded_customers_list, form=form)
        flash(f'Customer {form.name.data} not found', 'error')
    # else:
    #     customers_list = None
    # Prevent stored XSS
    # for customer in customers_list:
    #     customer.name = SecLib().prevent_xss_encoding(customer.name)
    #     customer.phone = SecLib().prevent_xss_encoding(customer.phone)
    #     customer.contact = SecLib().prevent_xss_encoding(customer.contact)
    return render_template("customers/customers.html", customers=None, form=form)
