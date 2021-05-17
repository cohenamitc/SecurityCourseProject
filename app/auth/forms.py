# Import Form and RecaptchaField (optional)
from flask_wtf import Form  # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, StringField, ValidationError

# Import Form validators
from wtforms.validators import Email, EqualTo, DataRequired, Optional
from app.config_service.config_service import ConfigService

import re

REQ_FIELD_MSG = 'This field is required'


class PasswordComplexityValidator(object):
    def __init__(self):
        c = ConfigService()
        self.length = c.get_password('length')
        if not c.get_password('complexity'):
            raise ValueError("Field 'complexity' not found in password config file")
        self.uppercase = c.get_password('complexity').get('uppercase', 0)
        self.lowercase = c.get_password('complexity').get('lowercase', 0)
        self.digits = c.get_password('complexity').get('digits', 0)
        self.special = c.get_password('complexity').get('special', 0)
        self.dictionary = c.get_password('dictionary')

    def _check_length(self, data):
        if len(data) < self.length:
            raise ValidationError(f'Password must be at least {self.length} long')

    def _check_complexity(self, data):
        # Check uppercase
        uppercase_pattern = r'[A-Z]'
        uppercase_count = len(re.findall(uppercase_pattern, data))
        if uppercase_count < self.uppercase:
            raise ValidationError(f'Password must contain at least {self.uppercase} uppercase letters')
        # Check lowercase
        lowercase_pattern = r'[a-z]'
        lowercase_count = len(re.findall(lowercase_pattern, data))
        if lowercase_count < self.lowercase:
            raise ValidationError(f'Password must contain at least {self.uppercase} lowercase letters')
        # Check digits
        digits_pattern = r'[0-9]'
        digits_count = len(re.findall(digits_pattern, data))
        if digits_count < self.digits:
            raise ValidationError(f'Password must contain at least {self.digits} digits')
        # Check special
        special_pattern = r'[^A-Za-z0-9]'
        special_count = len(re.findall(special_pattern, data))
        if special_count < self.special:
            raise ValidationError(f'Password must contain at least {self.special} special characters')

    def _check_dictionary(self, data):
        for word in self.dictionary:
            pattern = r'(?i).*%s.*' % word
            found = len(re.findall(pattern, data)) > 0
            if found:
                raise ValidationError('Password contains illegal words')

    def __call__(self, form, field):
        self._check_length(field.data)
        self._check_complexity(field.data)
        self._check_dictionary(field.data)


# Define the login form (WTForms)
class LoginForm(Form):
    # Input validation
    # email = StringField('Email Address', [Email(), DataRequired(message=REQ_FIELD_MSG)])

    # Not safe mail field (No input validation)
    email = StringField('Email Address', [DataRequired(message=REQ_FIELD_MSG)])
    password = PasswordField('Password', [DataRequired(message=REQ_FIELD_MSG)])


class SignUpForm(Form):
    email = StringField('Email Address', [Email(), DataRequired(message=REQ_FIELD_MSG)])
    password = PasswordField('Password', [PasswordComplexityValidator(), DataRequired(message=REQ_FIELD_MSG)])
    password_confirm = PasswordField('Confirm Password', [DataRequired(message=REQ_FIELD_MSG), EqualTo('password')])
    name = StringField('Full Name', [DataRequired(message=REQ_FIELD_MSG)])
    company = StringField('Company', [Optional()])


class ChangePasswordForm(Form):
    email = StringField('Email Address', [Email(), DataRequired(message=REQ_FIELD_MSG)])
    password = PasswordField('Current Password', [DataRequired(message=REQ_FIELD_MSG)])
    new_pass = PasswordField('New Password', [PasswordComplexityValidator(), DataRequired(message=REQ_FIELD_MSG)])
    new_pass_confirm = PasswordField('Confirm New Password', [DataRequired(message=REQ_FIELD_MSG), EqualTo('new_pass')])


class ForgotPassword(Form):
    email = StringField('Email Address', [Email(), DataRequired(message=REQ_FIELD_MSG)])


class ResetPasswordForm(Form):
    password = PasswordField('Password', [PasswordComplexityValidator(), DataRequired(message=REQ_FIELD_MSG)])
    password_confirm = PasswordField('Confirm Password', [DataRequired(message=REQ_FIELD_MSG), EqualTo('password')])
