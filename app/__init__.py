# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.auth.controllers import auth
from app.index.controllers import index
from app.admin_page.controllers import admin_page
from app.customers.controllers import comm_customers
from app.plans.controllers import comm_plans
from app.sectors.controllers import comm_sectors

# Register blueprint(s)
app.register_blueprint(auth)
app.register_blueprint(index)
app.register_blueprint(admin_page)
app.register_blueprint(comm_customers)
app.register_blueprint(comm_plans)
app.register_blueprint(comm_sectors)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
