# -*- coding: utf-8 -*-

from wtforms import TextField, validators, IntegerField
from wtforms.ext.sqlalchemy.orm import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import TextAreaField, FileField
from sambandid.models import Beer, User


class BeerForm(Form):
    name = TextField(u'Nafn', [validators.Length(min=2, max=80)])
    price = TextField(u'Verð')
    image = FileField(u'Mynd')


class BeerTransactionForm(Form):
    user = QuerySelectField(u'Félagsmaður', query_factory=lambda: User.query.all())
    beer = QuerySelectField(u'Bjór', query_factory=lambda: Beer.query.all())


class DepositTransactionForm(Form):
    user = QuerySelectField(u'Félagsmaður', query_factory=lambda: User.query.all())
    amount = IntegerField(u'Upphæð')
    comment = TextAreaField(u'Skýring')