# -*- coding: utf-8 -*-

"""
    application
    ~~~~~~~~~~~

    Application initialization and registrations

    :copyright: (c) 2012 by Roman Semirook.
    :license: BSD, see LICENSE for more details.
"""

from kit.helpers import AppFactory
from settings import DevelopmentConfig, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from flaskext.oauth import OAuth

# It's your main flask app. Define your own config class in settings.py
app = AppFactory(DevelopmentConfig).get_app()
app.secret_key = 'some_secret'

# Leave these imports here to avoid some problems with circular imports
from database import *

# Leave these methods here to avoid some problems with circular imports
app.register_all_blueprints()
app.register_all_context_processors()

oauth = OAuth()
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

# Application's views
from views import *
