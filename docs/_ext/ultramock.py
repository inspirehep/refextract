# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Hijacks `mock` to fake as many non-available modules as possible."""
import sys
import types

try:
    import unittest.mock as mock
except ImportError:
    import mock

# skip `_is_magic` check.
orig_is_magic = mock._is_magic
def always_false(*args, **kwargs):
    return False


# avoid spec configuration for mocked classes with super classes.
# honestly this does not happen very often and is kind of a tricky case.
orig_mock_add_spec = mock.NonCallableMock._mock_add_spec
def mock_add_spec_fake(self, spec, spec_set):
    orig_mock_add_spec(self, None, None)


# special MagicMock with empty docs
class MyMagicMock(mock.MagicMock):
    """"""


# set up a fake class-metaclass hierarchy
class SuperMockMetaMeta(MyMagicMock):
    __metaclass__ = MyMagicMock()


class SuperMockMeta(MyMagicMock):
    __metaclass__ = SuperMockMetaMeta


class SuperMock(MyMagicMock):
    __metaclass__ = SuperMockMeta


class MockedModule(types.ModuleType):
    def __init__(self, name):
        super(types.ModuleType, self).__init__(name)
        self.__name__ = super.__name__
        self.__file__ = self.__name__.replace('.', '/') + '.py'
        sys.modules[self.__name__] = self

    def __getattr__(self, key):
        obj = SuperMock
        setattr(self, key, obj)
        return obj


# overwrite imports
orig_import = __import__
def import_mock(name, *args, **kwargs):
    try:
        return orig_import(name, *args, **kwargs)
    except ImportError:
        return MockedModule(name)
import_patch = mock.patch('__builtin__.__import__', side_effect=import_mock)


# public methods
def activate():
    mock._is_magic = always_false
    mock.NonCallableMock._mock_add_spec = mock_add_spec_fake
    import_patch.start()


def deactivate():
    import_patch.stop()
    mock.NonCallableMock._mock_add_spec = orig_mock_add_spec
    mock._is_magic = orig_is_magic
