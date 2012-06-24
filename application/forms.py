# -*- coding: utf-8 -*-

from wtforms import TextField, PasswordField, validators, IntegerField
from wtforms.ext.sqlalchemy.orm import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.ext.appengine.db import model_form
from application.models import Beer, User

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


class BeerTransactionForm(Form):
    user = QuerySelectField(label='Member', query_factory=lambda: User.query.all())
    beer = QuerySelectField(label='Beer', query_factory=lambda: Beer.query.all())


class DepositTransactionForm(Form):
    user = QuerySelectField(label='Member', query_factory=lambda: User.query.all())
    amount = IntegerField('Amount')