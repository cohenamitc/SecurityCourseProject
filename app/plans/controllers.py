# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
comm_plans = Blueprint('plans', __name__, url_prefix='/plans')


# Set the route and accepted methods
@comm_plans.route('/')
def plans():
    return render_template("plans/plans.html")
