# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
comm_customers = Blueprint('customers', __name__, url_prefix='/customers')


# Set the route and accepted methods
@comm_customers.route('/')
def customers():
    return render_template("customers/customers.html")
