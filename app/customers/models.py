# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db
from uuid import uuid4


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.String(40), primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


# Define a User model
class Customer(Base):

    __tablename__ = 'customers'

    name = db.Column(db.String(128),  nullable=False)
    contact = db.Column(db.String(128),  nullable=False)
    phone = db.Column(db.String(128),  nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, contact, phone):
        self.name = name
        self.contact = contact
        self.phone = phone
        self.id = str(uuid4())

    def __repr__(self):
        return '<User %r>' % self.name
