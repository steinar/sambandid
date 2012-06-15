# -*- coding: utf-8 -*-

"""
    settings
    ~~~~~~~~

    Global settings for your project.

    :copyright: (c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

class BaseConfig(object):
    """Base config class"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Optional config for development needs.
    Make your own like this, inherit from BaseConfig class.
    """
    DEBUG = True
    TESTING = True


# The name of the package which contains your main application instance.
# Flask Kit helpers will look for app object in it.
APP_PACKAGE = 'application'

DB_PATH = '/tmp/test.db'


# If you will use some blueprints in your project (and you have to), register
# them in INSTALLED_BLUEPRINTS list. For example, if you have blueprint object
# like `simple_page = Blueprint('simple_page', __name__)` in the `simple_page`
# blueprint package, add it's name to the list (not the blueprint object itself).
INSTALLED_BLUEPRINTS = []


# Django-style for registering context processors.
CONTEXT_PROCESSORS = ['application.context_processors.my_email']

FACEBOOK_APP_ID = '475817332444834'
FACEBOOK_APP_SECRET = ''
try:
    from private import *
except ImportError:
    print "File private.py (should contain the facebook secret) is missing"
