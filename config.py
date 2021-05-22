import os

# Statement for enabling the development environment
DEBUG = os.environ.get("FLASK_ENV", "") == "development"

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_ECHO = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = int(os.environ.get("FLASK_THREADS_PER_PAGE", 2))

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = int(os.environ.get("FLASK_CSRF_ENABLED", 1)) == 1

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.environ["FLASK_CSRF_SESSION_KEY"]

# Secret key for signing cookies
SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
