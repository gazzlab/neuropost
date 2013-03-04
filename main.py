#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json
from types import FunctionType
from flask import Flask, render_template, Response, request, redirect
from flask.ext.login import (
  LoginManager,
  login_required,
  login_user,
  current_user,
  logout_user,
  )
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from xerblin import World, items
from sooper_sekrit import secret


W = World()


WEBFACTION_TEMPLATES = '/home/calroc/webapps/smlaum/templates'
OPENID_STORE = '/tmp/oid.store'


if os.path.exists(WEBFACTION_TEMPLATES):
  app = Flask(__name__, template_folder=WEBFACTION_TEMPLATES)
  sqlite_db_file = 'sqlite:///:memory:'
else:
  app = Flask(__name__)
  app.debug = True
  sqlite_db_file = 'sqlite:////tmp/test.db'


app.secret_key = secret
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_db_file
db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    name = db.Column(db.String(50))
    fullname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(12))

    def __init__(self, name, fullname, email, password):
        self.name = name
        self.fullname = fullname
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        assert self.id is not None
        return unicode(self.id)


login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(uid):
  try:
    uid = int(uid)
  except ValueError:
    return None
  return User.query.filter_by(id=uid).first()


oid = OpenID(app, OPENID_STORE)


@app.route("/")
def x():
  return render_template('main.html')


@app.route("/foo")
@login_required
def foo():
  return render_template('xerblin.html', foo=True)


def _p(n):
  '''Convert functions into JSON representations.'''
  if isinstance(n, FunctionType):
    return {
      'class': '__function__',
      'name': n.__name__,
      }


def as_json(w):
  '''
  Return the current state of the World object w as a JSON string.
  Functions are converted to JS objects containing the functions' names.
  '''
  stack, dictionary = w.getCurrentState()
  dictionary = list(name for name, function in items(dictionary))
  return json.dumps((stack, dictionary), default=_p, indent=2)


def get_session(request):
  '''
  Return the World object for the request's session.
  (This is currently a stub that just returns the module
  global World.)
  '''
  return W


@app.route("/step", methods=['POST'])
def step():
  command = request.form['command']
  w = get_session(request)
  w.step(command.split())
  res = as_json(w)
  return Response(
    response='{"result":%s}' % (res,),
    mimetype='application/json',
    )


@app.route("/login", methods=["GET", "POST"])
@oid.loginhandler
def login():
  if request.method == 'GET':
    if current_user.is_anonymous():
      return render_template(
        'login.html',
        next=oid.get_next_url(),
        error=oid.fetch_error()
        )
    return redirect('/logout')

  open_id = request.form.get('openid')
  if open_id:
    return oid.try_login(open_id, ask_for=['email', 'fullname', 'nickname'])

  username = request.form['user']
  pw = request.form['pasw']
  user = User.query.filter_by(name=username, password=pw).first()

  if user:
    login_user(user)
    return redirect(oid.get_next_url() or '/')
  return redirect('/Bah')


@app.route("/logout", methods=["GET", "POST"])
def logout():
  if not current_user.is_anonymous():
    if request.method == 'GET':
      return render_template('logout.html')
    logout_user()
  return redirect('/login')


@oid.after_login
def after_login(response):
  email_address = response.email
  if not email_address:
    flash('Invalid login. Please try again.')
    return redirect('/login')

  user = User.query.filter_by(email=email_address).first()
  if not user:
      nickname = response.nickname or email_address.split('@', 1)[0]
      user = User(
        name=nickname,
        fullname=response.fullname,
        email=email_address,
        password="",
        )
      db.session.add(user)
      db.session.commit()

  login_user(user)
  return redirect(oid.get_next_url() or '/')


if __name__ == "__main__":
  app.run()
