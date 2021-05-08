# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, StringField

# Import Form validators
from wtforms.validators import Email, EqualTo, DataRequired, Optional


REQ_FIELD_MSG = 'This field is required'


# Define the login form (WTForms)
class SearchCustomer(Form):
    name = StringField('name', [DataRequired(message=REQ_FIELD_MSG)])
