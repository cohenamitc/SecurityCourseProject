# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, StringField

# Import Form validators
from wtforms.validators import Email, EqualTo, DataRequired, Optional


REQ_FIELD_MSG = 'This field is required'


# Define the login form (WTForms)
class LoginForm(Form):
    email = StringField('Email Address', [Email(), DataRequired(message=REQ_FIELD_MSG)])
    password = PasswordField('Password', [DataRequired(message=REQ_FIELD_MSG)])


class SignUpForm(Form):
    email = StringField('Email Address', [Email(), DataRequired(message=REQ_FIELD_MSG)])
    password = PasswordField('Password', [DataRequired(message=REQ_FIELD_MSG)])
    password_confirm = PasswordField('Confirm Password', [DataRequired(message=REQ_FIELD_MSG), EqualTo('password')])
    name = StringField('Full Name', [DataRequired(message=REQ_FIELD_MSG)])
    company = StringField('Company', [Optional()])


class ChangePasswordForm(Form):
    email = StringField('Email Address', [Email(), DataRequired(message=REQ_FIELD_MSG)])
    password = PasswordField('Current Password', [DataRequired(message=REQ_FIELD_MSG)])
    # TODO:insert password complexity validator here
    new_pass = PasswordField('New Password', [DataRequired(message=REQ_FIELD_MSG)])
    new_pass_confirm = PasswordField('Confirm New Password', [DataRequired(message=REQ_FIELD_MSG), EqualTo('new_pass')])


class ForgotPassword(Form):
    email = StringField('Email Address', [Email(), DataRequired(message=REQ_FIELD_MSG)])


class ResetPasswordForm(Form):
    password = PasswordField('Password', [DataRequired(message=REQ_FIELD_MSG)])
    password_confirm = PasswordField('Confirm Password', [DataRequired(message=REQ_FIELD_MSG), EqualTo('password')])
