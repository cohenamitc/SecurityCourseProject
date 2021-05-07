# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
admin_page = Blueprint('admin_page', __name__, url_prefix='/admin')


# Set the route and accepted methods
@admin_page.route('/')
def manager():
    return render_template("manager/manager.html")
