# -*- coding: utf-8 -*-
#
# This file is part of refextract
# Copyright (C) 2016, 2018 CERN.
#
# refextract is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# refextract is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with refextract; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

from refextract.references.find import get_reference_section_beginning


def test_simple():
    sect = get_reference_section_beginning([
        "Hello",
        "References",
        "[1] Ref1"
    ])
    assert sect == {
        'marker': '[1]',
        'marker_pattern': u'\\s*(?P<mark>\\[\\s*(?P<marknum>\\d+)\\s*\\])',
        'start_line': 1,
        'title_string': 'References',
        'title_marker_same_line': False,
        'how_found_start': 1,
    }


def test_no_section():
    sect = get_reference_section_beginning("")
    assert sect is None


def test_no_title_via_brackets():
    sect = get_reference_section_beginning([
        "Hello",
        "[1] Ref1"
        "[2] Ref2"
    ])
    assert sect == {
        'marker': '[1]',
        'marker_pattern': u'(?P<mark>(?P<left>\\[)\\s*(?P<marknum>\\d+)\\s*(?P<right>\\]))',
        'start_line': 1,
        'title_string': None,
        'title_marker_same_line': False,
        'how_found_start': 2,
    }


def test_no_title_via_dots():
    sect = get_reference_section_beginning([
        "Hello",
        "1. Ref1"
        "2. Ref2"
    ])
    assert sect == {
        'marker': '1.',
        'marker_pattern': u'(?P<mark>(?P<left>)\\s*(?P<marknum>\\d+)\\s*(?P<right>\\.))',
        'start_line': 1,
        'title_string': None,
        'title_marker_same_line': False,
        'how_found_start': 3,
    }


def test_no_title_via_numbers():
    sect = get_reference_section_beginning([
        "Hello",
        "1 Ref1"
        "2 Ref2"
    ])
    assert sect == {
        'marker': '1',
        'marker_pattern': u'(?P<mark>(?P<left>)\\s*(?P<marknum>\\d+)\\s*(?P<right>))',
        'start_line': 1,
        'title_string': None,
        'title_marker_same_line': False,
        'how_found_start': 4,
    }


def test_no_title_via_numbers2():
    sect = get_reference_section_beginning([
        "Hello",
        "1",
        "Ref1",
        "(3)",
        "2",
        "Ref2",
    ])
    assert sect, {
        'marker': '1',
        'marker_pattern': u'(?P<mark>(?P<left>)\\s*(?P<marknum>\\d+)\\s*(?P<right>))',
        'start_line': 1,
        'title_string': None,
        'title_marker_same_line': False,
        'how_found_start': 4,
    }
