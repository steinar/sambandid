from wtforms import Form, BooleanField, TextField, PasswordField, validators
from wtforms.ext.appengine.db import model_form
from application.models import Beer

class RegistrationForm(Form):
    user = TextField('Username', [validators.Length(min=2, max=35)])
    name = TextField('Name', [validators.Length(min=2, max=80)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class BeerForm(Form):
    name = TextField('Name', [validators.Length(min=2, max=80)])
    price = TextField('Price')

