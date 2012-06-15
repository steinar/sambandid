# -*- coding: utf-8 -*-

from application.database import db
from datetime import datetime
# Put your main models here

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    registration_date = db.Column(db.DateTime)


    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

        self.registration_date = datetime.utcnow()


    def __repr__(self):
        return '<User %r>' % self.username


class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Integer)
    add_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)

    def __init__(self, name='', price=''):
        self.name = name
        self.price = price
        self.add_date = datetime.utcnow()


    def __repr__(self):
        return '<Beer %r>' % self.name


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    registered_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref='purchases', lazy='dynamic', primaryjoin='User.id==Purchase.user_id')
    registered_by = db.relationship('User', backref='registrations', lazy='dynamic', primaryjoin='User.id==Purchase.registered_by_id')

    beer_id = db.Column(db.Integer, db.ForeignKey('beer.id'))
    beer = db.relationship('Beer', backref='purchases', lazy='dynamic')

    purchase_date = db.Column(db.DateTime)

    def __init__(self, user, registered_by, beer):
        self.user = [user]
        self.registered_by = [registered_by]
        self.beer = [beer]

        self.purchase_date = datetime.utcnow()




