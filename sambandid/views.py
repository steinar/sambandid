# -*- coding: utf-8 -*-
from datetime import date, timedelta
import os
from werkzeug.utils import redirect
from flask import send_from_directory
from flask import session
from flask.ext.oauth import OAuthException
from flask.globals import request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask.views import View, MethodView
#from flask.ext.admin.contrib.sqlamodel.view import ModelView
from sambandid import app, facebook, photos#, admin
from sambandid.database import db
from sambandid.forms import BeerForm, BeerTransactionForm, DepositTransactionForm
from sambandid.models import Beer, User, Transaction


# Helper functions

def get_user_object(username=None):
    username = username or 'user' in session and session['user']['username']
    if username:
        return User.query.filter_by(username=username, active=True).first()
    return None


def inject_user(func):
    def f(*args,**kwargs):
        if not 'user' in session:
            return redirect(url_for("login-required"))
        user = get_user_object()
        if 'user' in session and not user:
            return redirect(url_for('logout'))
        return func(*args, user=user,**kwargs)
    f.__name__ = func.__name__
    return f


def only_admin(func):
    def f(*args,**kwargs):
        user = 'user' in kwargs and kwargs['user'] or get_user_object()
        if not user.is_admin:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
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
@app.errorhandler(OAuthException)
def logout(sme=None):
    session.pop('user', None)
    session.pop('oauth_token', None)
    session.pop('_flashes', None)
    flash(u'Þú hefur aftengst.')
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
@inject_user
def index(user=None):
    token = get_facebook_oauth_token()
    if 'user' in session and not user:
        return redirect('logout')
    recent_transactions = Transaction.query.order_by(Transaction.transaction_date.desc()).limit(10)

    return render_template('main.html', token=token, user=user and user.as_dict(), recent_transactions=recent_transactions)


def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Beer!

class BeerAddView(MethodView):
    @inject_user
    def get(self, beer_id=None, user=None):
        if beer_id:
            beer = Beer.query.filter_by(id=beer_id).first()
        else:
            beer = Beer()
        form = BeerForm(obj=beer)
        return render_template('beer_form.html', form=form)

    @inject_user
    def post(self, beer_id=None, user=None):
        form = BeerForm(request.form)
        if beer_id:
            beer = Beer.query.filter_by(id=beer_id).first()
        else:
            beer = Beer()
        if 'image' in request.files and request.files['image']:
            beer.image_path = photos.save(request.files['image'])
        form.populate_obj(beer)
        beer.update_energy()
        db.session.add(beer)
        db.session.commit()
        flash('Saved')
        return redirect(url_for("beers"))

app.add_url_rule('/beer/add', view_func=BeerAddView.as_view('beer_add'))
app.add_url_rule('/beer/edit/<int:beer_id>/', view_func=BeerAddView.as_view('beer_edit'))


@app.route('/beers')
@inject_user
def beers(user=None):
    beers = Beer.all_active()
    beers_inactive = Beer.all_inactive()
    return render_template('beers.html', beers=beers, beers_inactive=beers_inactive)


# Transactions

@app.route('/transactions')
@inject_user
def transactions(user=None):
#    transactions_by_me = Transaction.query.filter_by(registered_by=user)
    my_transactions = Transaction.query.filter_by(user=user).order_by(Transaction.transaction_date.desc())
    account_status = user.account_status
    return render_template('transactions.html', my_transactions=my_transactions, account_status=account_status)


@app.route('/transactions/recent')
@inject_user
def recent_transactions(user=None):
    recent_plus = Transaction.query.filter(Transaction.amount>0).order_by(Transaction.transaction_date.desc()).limit(200)
    recent_minus = Transaction.query.filter(Transaction.amount<0).order_by(Transaction.transaction_date.desc()).limit(200)
    return render_template('recent_transactions.html', user=user, recent_minus=recent_minus, recent_plus=recent_plus)


@app.route('/transaction/<int:beer_id>')
@inject_user
def beer_transaction(beer_id, user=None):
    beer = Beer.query.filter_by(id=beer_id).first()
    initial = Transaction(user=user, beer=beer)
    beer_form = BeerTransactionForm(obj=initial)
    return render_template('transaction_form.html', beer_form=beer_form, deposit_form=None)


class TransactionRegistrationView(MethodView):
    @inject_user
    def get(self, user=None):
        initial = Transaction(user=user, amount=None)
        beer_form = BeerTransactionForm(obj=initial)
        deposit_form = DepositTransactionForm(obj=initial)
        return render_template('transaction_form.html', beer_form=beer_form, deposit_form=deposit_form)

    @inject_user
    def post(self, user=None):
        if not request.form or (not 'beer' in request.form and not 'deposit' in request.form):
            return redirect(url_for("transaction-add"))

        form_cls = BeerTransactionForm if 'beer' in request.form else DepositTransactionForm
        form = form_cls(request.form)
        transaction = Transaction(**form.data)
        transaction.registered_by = user
        transaction.save()
        transaction.user.update_account_status()
        flash(unicode('Færslan hefur verið bókfærð. Þakka þér, meistari.', 'utf-8'))
        return redirect(url_for("transactions"))

app.add_url_rule('/transactions/add', view_func=TransactionRegistrationView.as_view('transaction_add'))

@app.route('/status-overview')
@inject_user
def status_overview(user=None):
    if 'refresh' in request.args:
        updates = [u.update_account_status() for u in User.query.all()]

    users = User.get_all()
    status_sum = sum(map(lambda x: x.account_status or 0, users))*(-1)
    return render_template('status_overview.html', users=users, status_sum=status_sum)



@app.route('/quick-transaction')
@inject_user
def quick_transaction(user=None):
    since = (date.today()-timedelta(weeks=16)).isoformat()
    users = (t.user for t in \
             Transaction.query.filter(Transaction.transaction_date >= since)\
                 .join(Transaction.user).group_by('user_id').order_by(User.name).all())
    return render_template('quick_transaction_members.html', users=users)

@app.route('/quick-transaction/<string:username>/')
@inject_user
def quick_transaction_beers(user=None, username=None):
    selected_user = get_user_object(username)
    beers = Beer.all_active()
    beers_inactive = Beer.all_inactive()
    return render_template('quick_transaction_beers.html', beers=beers, beers_inactive=beers_inactive,
                           selected_user=selected_user)

@app.route('/quick-transaction/<string:username>/<int:beer_id>/')
@inject_user
def quick_transaction_post(user=None, username=None, beer_id=None):
    selected_user = get_user_object(username)
    beer = Beer.query.filter_by(id=beer_id).first()
    transaction = Transaction(user=selected_user, registered_by=user, beer=beer)
    transaction.save()
    transaction.user.update_account_status()
    flash(u'Skráði %s á %s' % (beer.name, selected_user.name))
    return redirect(url_for('quick_transaction'))


# Admin

def authenticated_admin_view(cls,name=None):
    return type(name or cls.__name__, (cls,), {'is_accessible': lambda self: get_user_object() and get_user_object().is_admin})

#admin.add_view(authenticated_admin_view(ModelView)(User, db.session))
#admin.add_view(authenticated_admin_view(ModelView)(Transaction, db.session))
