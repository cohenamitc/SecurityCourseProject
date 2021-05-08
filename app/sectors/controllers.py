# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import login_required
# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
comm_sectors = Blueprint('sectors', __name__, url_prefix='/sectors')


# Set the route and accepted methods
@comm_sectors.route('/')
@login_required
def sectors():
    return render_template("sectors/sectors.html")
