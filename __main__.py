# -*- coding: utf-8 -*-
#
#    Copyright © 2012 Simon Forman
#
#    This file is part of Pigeon Computer.
#
#    Pigeon Computer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Pigeon Computer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Pigeon Computer.  If not, see <http://www.gnu.org/licenses/>.
#
from os.path import expanduser, exists, join
from argparse import ArgumentParser
from pickle import Unpickler
import logging, sys


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


# First parse command line args if any.
parser = ArgumentParser()
parser.add_argument(
  '-r', '--roost',
  default=expanduser('~/.pigeon'),
  help=('Use this directory as home for the Pigeon system. (default: %(default)s).\n'
        '(I apologize for the terrible pun.)'),
  )
parser.add_argument(
  '-i', '--init',
  default=False,
  action='store_true',
  help=('Initialize the "roost" directory with git repo, log, system.pickle '
        'and default config file.  '
        "If '--no-config' is passed the default config file will NOT be "
        'created.)'
        ),
  )
args = parser.parse_args()


if not exists(args.roost):
  print "Roost directory %r doesn't exist!" % (args.roost,)
  sys.exit(2)


# Initialize the "roost" directory if requested.
if args.init:
  from Xerblin.gitstore import initialize_repo, list_words, SYSTEM_PICKLE
  from Xerblin.xerblin import ROOT
  text = list_words(ROOT[1])
  initialize_repo(args.roost, ROOT, text, not args.no_config)


state_file_name = join(args.roost, SYSTEM_PICKLE)
try:
  with open(state_file_name) as f:
    up = Unpickler(f)
    # Pull out all the sequentially saved state, command, state, ... data.
    # This loop will break after the last saved state is loaded leaving
    # the last saved state in the 'state' variable
    while True:
      try:
        state = up.load()
      except EOFError:
        break
except IOError, e:
  print e
  print 'Did you initialize roost? (Use "--init" command.)'
  sys.exit(e.errno)


# Create a commit_thing to let us save our state to the git repo after
# changes.
from Xerblin.gitstore import make_commit_thing
try:
  commit_thing = make_commit_thing(args.roost, [SYSTEM_PICKLE])
except ValueError, e:
  print e
  print 'Did you initialize roost? (Use "--init" command.)'
  sys.exit(2)


# Now that the config_file has had a chance to do its thing, import the
# system and run.
from Xerblin.gitstore import CommitWorld
w = CommitWorld(
  initial=state,
  save_file=state_file_name,
  commit_thing=commit_thing,
  )


import Xerblin.main
Xerblin.main.W = w
Xerblin.main.app.run(debug=True)
