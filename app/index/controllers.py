# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from flask_login import current_user, login_required

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db, LoginManager

# Define the blueprint: 'auth', set its url prefix: app.url/auth
index = Blueprint('index', __name__)


# Set the route and accepted methods
@index.route('/')
def home():
    return render_template("index/index.html", user=current_user)
