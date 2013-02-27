#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json
from types import FunctionType
from flask import Flask, render_template, Response, request
from flask.ext.login import LoginManager
from xerblin import World, items
from data_models import load_user
from sooper_sekrit import secret


W = World()


WEBFACTION_TEMPLATES = '/home/calroc/webapps/smlaum/templates'


if os.path.exists(WEBFACTION_TEMPLATES):
  app = Flask(__name__, template_folder=WEBFACTION_TEMPLATES)
else:
  app = Flask(__name__)
  app.debug = True


app.secret_key = secret
login_manager = LoginManager()
login_manager.setup_app(app)
load_user = login_manager.user_loader(load_user)


@app.route("/")
def x():
  return render_template('main.html')


@app.route("/foo")
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


if __name__ == "__main__":
  app.run(debug=True)
