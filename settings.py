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

SECRET_KEY = 'mmmmm bjor'

INSTALLED_BLUEPRINTS = []

CONTEXT_PROCESSORS = ['sambandid.context_processors.my_email']

FACEBOOK_APP_ID = '475817332444834'
FACEBOOK_APP_SECRET = ''

UPLOADS_DEFAULT_DEST = '%s/sambandid/static/data' % BASE_PATH
UPLOADS_DEFAULT_URL = '/static/data/'

try:
    from private import *
except ImportError:
    print "File private.py (should contain the facebook secret) is missing"
