# -*- coding: utf-8 -*-

from kit.helpers import AppFactory
from settings import DevelopmentConfig, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from flaskext.oauth import OAuth
import settings

app = AppFactory(DevelopmentConfig).get_app()
app.secret_key = settings.SECRET_KEY

from database import *

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
