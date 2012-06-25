# -*- coding: utf-8 -*-
import math
import os
from sqlalchemy.exc import OperationalError
from sambandid import photos

from sambandid.database import db
from datetime import datetime
# Put your main models here
from settings import DB_PATH

class SaveMixIn(object):
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except OperationalError, e:
            db.session.rollback()
            raise RuntimeError(e)


class User(SaveMixIn, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    account_status = db.Column(db.Integer)

    registration_date = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email

        self.registration_date = datetime.utcnow()


    def __repr__(self):
        return '<User %r>' % self.username

    def __unicode__(self):
        return self.name

    @classmethod
    def from_facebook(cls, me):
        user = User.query.filter_by(username=me.data['username']).first()
        if not user:
            user = User(me.data['name'], me.data['username'], me.data['email'])
            db.session.add(user)
            db.session.commit()
        return user

    def update_account_status(self):
        amounts = map(lambda t: t.amount, Transaction.query.filter_by(user=self).all())
        self.account_status = sum(amounts) if amounts else 0
        self.save()

    def as_dict(self):
        return {'id': self.id, 'name': self.name, 'username': self.username, 'email': self.email, \
                'account_status': self.account_status }

class Beer(SaveMixIn, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Integer)
    image_path = db.Column(db.String(250))
    add_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name='', price=''):
        self.name = name
        self.price = price
        self.add_date = datetime.utcnow()

    @property
    def image_url(self):
        if not self.image_path:
            return None
        return photos.url(self.image_path)

    @classmethod
    def all_active(cls):
        return Beer.query.filter_by(active=True)

    def __repr__(self):
        return '<Beer %r>' % self.name

    def __unicode__(self):
        return unicode("%s (%s)" % (self.name,self.price))



class Transaction(SaveMixIn, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    registered_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='transations', lazy='immediate', primaryjoin='User.id==Transaction.user_id')
    registered_by = db.relationship('User', backref='registrations', lazy='immediate', primaryjoin='User.id==Transaction.registered_by_id')

    beer_id = db.Column(db.Integer, db.ForeignKey('beer.id'), nullable=True)
    beer = db.relationship('Beer', backref='transations', lazy='immediate')

    amount = db.Column(db.Integer, default=0)

    comment = db.Column(db.Unicode)

    transaction_date = db.Column(db.DateTime)

    def __init__(self, user=None, registered_by=None, beer=None, amount=None, comment=''):
        self.user = user
        self.registered_by = registered_by
        self.beer = beer
        self.amount = beer and beer.price and -beer.price or amount or None
        self.transaction_date = datetime.utcnow()
        self.comment = comment


    def __repr__(self):
        return '<Transaction %s, %s, %s, %s>' % (self.user, self.registered_by, self.beer, self.amount)

    def __unicode__(self):
        return unicode(self.transaction_date)


#if not os.path.exists(DB_PATH):
db.create_all()


