# -*- coding: utf-8 -*-
from flask import session
from flask.globals import request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask.views import View, MethodView
from werkzeug.utils import redirect
from application import app, facebook


# Your main views may be here. In fact, all of your views may be here
# if you don't use blueprints and your site is really micro.

# In this example we use so called `Pluggable Views` or `Class Based Views`.
# You should be familiar with them if you already had some experience with Django.
# If not - please, visit http://flask.pocoo.org/docs/views/
from application.database import db
from application.forms import RegistrationForm, BeerForm
from application.models import Beer, User

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
            )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    session['user'] = User.from_facebook(me).as_dict()
    return redirect('/')
    return 'Logged in as id=%s name=%s redirect=%s' %\
           (me.data['id'], me.data['name'], request.args.get('next'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('oauth_token', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

class MainPageView(View):
    def dispatch_request(self):
        form = RegistrationForm()
        token = get_facebook_oauth_token()
        return render_template('main.html', form=form, token=token)
app.add_url_rule('/', view_func=MainPageView.as_view('main_page'))

class RegisterView(View):
    def dispatch_request(self):
        form = RegistrationForm()
        return render_template('register.html', form=form)

# Good style is to place your view URL rules right after the view definition.
app.add_url_rule('/register', view_func=RegisterView.as_view('register'))

class BeerAddView(MethodView):
    def get(self):
        form = BeerForm()
        return render_template('beer_form.html', form=form)

    def post(self):
        form = BeerForm(request.form)
        beer = Beer()
        form.populate_obj(beer)
        db.session.add(beer)
        db.session.commit()
        flash('Saved')
        return redirect(url_for("beers"))


app.add_url_rule('/beer/add', view_func=BeerAddView.as_view('beer_add'))


class BeersView(View):
    def dispatch_request(self):
        beers = Beer.query.all()
        return render_template('beers.html', beers=beers)


app.add_url_rule('/beers', view_func=BeersView.as_view('beers'))