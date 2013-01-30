# -*- coding: utf-8 -*-
#
#    Copyright © 2013 Simon Forman
#
#    This file is Xerblin.
#
#    Xerblin is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Xerblin is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Xerblin.  If not, see <http://www.gnu.org/licenses/>.
#
from xerblin import World, items
from types import FunctionType
import json


##_D = dict(words)
##for w in (handle_sequence, handle_branch, handle_loop, enstacken):
##  _D[w.__name__] = w


def p(n):
  '''
  Convert functions into JSON representations.
  '''
  if isinstance(n, FunctionType):
    return {
      'class': '__function__',
      'name': n.__name__,
      }


##def q(o):
##  if o.get('class') == '__function__':
##    return _D[o['name']]
##  return o
##
##
##print json.loads(s, object_hook=q)


W = World()


def as_json(w=W):
  stack, dictionary = w.getCurrentState()
  dictionary = list(name for name, function in items(dictionary))
  return json.dumps((stack, dictionary), default=p, indent=2)


def get_session(request):
  return W
