# -*- coding: utf-8 -*-

from wtforms import TextField, validators, IntegerField, FloatField, SelectField
from wtforms.ext.sqlalchemy.orm import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import TextAreaField, FileField
from wtforms.fields.core import BooleanField
from sambandid.models import Beer, User


class BeerForm(Form):
    name = TextField(u'Nafn', [validators.Length(min=2, max=80)])
    name_accusative = TextField(u'Nafn þf.', [validators.Length(min=2, max=80)])
    price = TextField(u'Verð')
    purchase_price = TextField(u'Innkaupsverð')
    volume = FloatField(u'Magn')
    alcohol = FloatField(u'Vínhlutfall')
    calories = FloatField(u'Kaloríur')
    joules = FloatField(u'Orka')
    image = FileField(u'Mynd')
    active = BooleanField(u'Virkur', default=True)


class BeerTransactionForm(Form):
    user = QuerySelectField(u'Félagsmaður', query_factory=lambda: User.get_all())
    beer = QuerySelectField(u'Bjór', query_factory=lambda: Beer.all_active())
    quantity = SelectField(u'Fjöldi', default=1, choices=[(x, x) for x in range(1, 13)])


class DepositTransactionForm(Form):
    user = QuerySelectField(u'Félagsmaður', query_factory=lambda: User.get_all())
    amount = IntegerField(u'Upphæð')
    comment = TextAreaField(u'Skýring')
