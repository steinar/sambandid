# -*- coding: utf-8 -*-

"""
    database
    ~~~~~~~~

    Database settings

    :copyright: (c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

# Set you database object here. For example, if you prefer MongoAlchemy ORM,
# define `db` object like this and use it wherever you need

from flask.ext.sqlalchemy import SQLAlchemy
from application import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


#db = MongoAlchemy(app)

