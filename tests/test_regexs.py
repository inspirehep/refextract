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

import re

from refextract.references import regexs


def test_word():
    r = regexs._create_regex_pattern_add_optional_spaces_to_word_characters('ABC')
    assert r == ur'A\s*B\s*C\s*'


def test_reference_section_title_pattern():
    r = regexs.get_reference_section_title_patterns()
    assert len(r) > 2


def test_get_reference_line_numeration_marker_patterns():
    r = regexs.get_reference_line_numeration_marker_patterns()
    assert len(r) > 2


def test_get_reference_line_marker_pattern():
    r = regexs.get_reference_line_marker_pattern('ABC')
    assert r.pattern.find('ABC') != -1


def test_get_post_reference_section_title_patterns():
    r = regexs.get_post_reference_section_title_patterns()
    assert len(r) > 2


def test_get_post_reference_section_keyword_patterns():
    r = regexs.get_post_reference_section_keyword_patterns()
    assert len(r) > 2


def test_regex_match_list():
    s = 'ABC'
    m = regexs.regex_match_list(s, [
        re.compile('C.C'),
        re.compile('A.C')
    ])
    assert m
    m = regexs.regex_match_list(s, [
        re.compile('C.C')
    ])
    assert m is None
