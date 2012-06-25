# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from sambandid import app
from settings import DB_PATH

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
db = SQLAlchemy(app)


