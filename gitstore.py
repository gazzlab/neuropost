#!/usr/bin/env python
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
import pickle, logging, sys
from os.path import exists, join
from dulwich.repo import Repo, NotGitRepository
from xerblin import World, items


SYSTEM_PICKLE = 'system.pickle'


class CommitWorldMixin(object):

  def __init__(self, *a, **b):
    self.commit_thing = b.pop('commit_thing')
    super(CommitWorldMixin, self).__init__(*a, **b)

  def setCurrentState(self, state):
    super(CommitWorldMixin, self).setCurrentState(state)
    self.commit_thing()


class CommitWorld(CommitWorldMixin, World, object):
    pass


def make_commit_thing(path, files):
  log = logging.getLogger('COMMIT')
  try:
    repo = Repo(path)
  except NotGitRepository:
    log.critical("%r isn't a repository!", path)
    raise ValueError("%r isn't a repository!" % (path,))

  # Note that we bind the args as defaults rather than via a closure so
  # you can override them later if you want.
  def commit(files=files, repo=repo, log=log):
    repo.stage(files)
    commit_sha = repo.do_commit('autosave')
    log.info('commit %s', commit_sha)

  return commit


def initialize_repo(path, state):
  log = logging.getLogger('INIT_REPO')
  if not exists(path):
    log.critical("%r doesn't exist!", path)
    raise ValueError("%r doesn't exist!" % (path,))

  try:
    Repo(path)
  except NotGitRepository:
    # Good! That's what we expect.
    repo = Repo.init(path)
    log.info('%r created.', repo)
  else:
    # No good! We are an initialize function, nothing else.
    log.critical('Repository already exists at %r', path)
    raise ValueError('Repository already exists at %r' % (path,))

  system_pickle_file_name = join(path, SYSTEM_PICKLE)
  pickle.dump(state, open(system_pickle_file_name, 'wb'))
  log.info('%s written.', system_pickle_file_name)

  repo.stage([SYSTEM_PICKLE])
  staged = list(repo.open_index())
  log.info('Files staged: ' + ', '.join(['%s'] * len(staged)), *staged)
  commit = repo.do_commit('Initial commit.')
  log.info('Initial commit done. %s', commit)
