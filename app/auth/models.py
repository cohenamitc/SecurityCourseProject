# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from uuid import uuid4
from flask_login import UserMixin


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.String(40), primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


# Define a User model
class User(Base, UserMixin):

    __tablename__ = 'auth_user'

    # User Name
    name = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email = db.Column(db.String(128),  nullable=False,
                      unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    status = db.Column(db.SmallInteger, nullable=False, default=1)

    company = db.Column(db.String(128), nullable=True)

    # New instance instantiation procedure
    def __init__(self, name, email, password, company=None):
        self.name = name
        self.email = email
        self.password = password
        self.company = company
        self.id = str(uuid4())

    def set_password(self, password):
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name


class History(Base):

    __tablename__ = 'pass_history'

    userid = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(192), nullable=False)

    def __init__(self, userid, password):
        self.userid = userid
        self.password = password
        self.id = str(uuid4())

    def __repr__(self):
        return '<History %r>' % self.id


class ResetPassword(Base):

    __tablename__ = 'reset_password'

    userid = db.Column(db.String(40), nullable=False)
    random_hash = db.Column(db.String(192), nullable=False)

    def __init__(self, userid, random_hash):
        self.userid = userid
        self.random_hash = random_hash
        self.id = str(uuid4())

    def __repr__(self):
        return '<Reset Password %r>' % self.id


class FailedLogin(Base):

    __tablename__ = 'failed_login'

    userid = db.Column(db.String(40), nullable=False)

    def __init__(self, userid):
        self.userid = userid
        self.id = str(uuid4())

    def __repr__(self):
        return '<Failed Login %r>' % self.id
