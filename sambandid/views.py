# -*- coding: utf-8 -*-
from flaskext.uploads import IMAGES, UploadSet
import os
from flask import session
from flask.globals import request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask.views import View, MethodView
from werkzeug.utils import redirect, secure_filename
from flask import send_from_directory

from sambandid import app, facebook, photos
from sambandid.database import db
from sambandid.forms import BeerForm, BeerTransactionForm, DepositTransactionForm
from sambandid.models import Beer, User, Transaction

# Helper functions

def get_user_object(username=None):
    username = username or 'user' in session and session['user']['username']
    if username:
        return User.query.filter_by(username=username).first()
    return None


def require_login(func):
    def f(*args,**kwargs):
        if not 'user' in session:
            return redirect(url_for("login-required"))
        return func(*args,**kwargs)
    f.__name__ = func.__name__
    return f


# Authentication

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


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('oauth_token', None)
    session.pop('_flashes', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


class LoginRequriedView(View):
    def dispatch_request(self):
        return render_template('login_required.html')
app.add_url_rule('/login-required', view_func=LoginRequriedView.as_view('login-required'))


# Front page

@app.route('/')
def index():
    token = get_facebook_oauth_token()
    user = get_user_object()
    if 'user' in session and not user:
        return redirect('logout')
    return render_template('main.html', token=token, user=user and user.as_dict())



def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Beer!

def allowed_file(filename):
    return '.' in filename and\
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class BeerAddView(MethodView):
    @require_login
    def get(self):
        form = BeerForm()
        return render_template('beer_form.html', form=form)


    @require_login
    def post(self):
        form = BeerForm(request.form)
        beer = Beer()
        print request.files
        if 'image' in request.files:
            beer.image_path = photos.save(request.files['image'])
        form.populate_obj(beer)
        db.session.add(beer)
        db.session.commit()
        flash('Saved')
        return redirect(url_for("beers"))

app.add_url_rule('/beer/add', view_func=BeerAddView.as_view('beer_add'))


@app.route('/beers')
def beers():
    beers = Beer.query.all()
    return render_template('beers.html', beers=beers)

# Transactions

@app.route('/transactions')
@require_login
def transactions():
    user = get_user_object()
    transactions_by_me = Transaction.query.filter_by(registered_by=user)
    my_transactions = Transaction.query.filter_by(user=user)
    account_status = user.account_status
    return render_template('transactions.html', transactions_by_me=transactions_by_me, \
        my_transactions=my_transactions, account_status=account_status)


@app.route('/transaction/<int:beer_id>')
@require_login
def beer_transaction(beer_id):
    beer = Beer.query.filter_by(id=beer_id).first()
    initial = Transaction(user=get_user_object(), beer=beer)
    beer_form = BeerTransactionForm(obj=initial)
    return render_template('transaction_form.html', beer_form=beer_form, deposit_form=None)


class TransactionRegistrationView(MethodView):
    @require_login
    def get(self):
        initial = Transaction(user=get_user_object(), amount=None)
        beer_form = BeerTransactionForm(obj=initial)
        deposit_form = DepositTransactionForm(obj=initial)
        return render_template('transaction_form.html', beer_form=beer_form, deposit_form=deposit_form)

    @require_login
    def post(self):
        if not request.form or (not 'beer' in request.form and not 'deposit' in request.form):
            return redirect(url_for("transaction-add"))

        form_cls = BeerTransactionForm if 'beer' in request.form else DepositTransactionForm
        form = form_cls(request.form)
        transaction = Transaction(**form.data)
        transaction.registered_by = get_user_object()
        transaction.save()
        user = get_user_object()
        user.update_account_status()
        flash(unicode('Færslan hefur verið bókfærð. Þakka þér, meistari.', 'utf-8'))
        return redirect(url_for("transactions"))

app.add_url_rule('/transactions/add', view_func=TransactionRegistrationView.as_view('transaction_add'))