# -*- coding: utf-8 -*-

import os

class BaseConfig(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

APP_PACKAGE = 'sambandid'

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DB_PATH = '%s/sambandid.db' % BASE_PATH

INSTALLED_BLUEPRINTS = []

CONTEXT_PROCESSORS = []

UPLOADS_DEFAULT_DEST = '%s/sambandid/static/data' % BASE_PATH
UPLOADS_DEFAULT_URL = '/static/data/'

# Set these in private.py
SECRET_KEY = ''
FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''

try:
    from private import *
except ImportError:
    print "File private.py (should contain the facebook secret and secret key) is missing"
