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

from refextract import extract_references_from_file
from refextract.references.text import (
    rebuild_reference_lines,
)


def test_simple():
    marker_pattern = ur"^\s*(?P<mark>\[\s*(?P<marknum>\d+)\s*\])"
    refs = [
        u"[1] hello",
        u"hello2",
        u"[2] foo",
    ]
    rebuilt_refs = rebuild_reference_lines(refs, marker_pattern)
    assert rebuilt_refs == [
        u"[1] hello hello2",
        u"[2] foo",
    ]


def test_pagination_non_removal():
    marker_pattern = ur"^\s*(?P<mark>\[\s*(?P<marknum>\d+)\s*\])"
    refs = [
        u"[1] hello",
        u"hello2",
        u"[2]",
        u"foo",
    ]
    rebuilt_refs = rebuild_reference_lines(refs, marker_pattern)
    assert rebuilt_refs == [
        u"[1] hello hello2",
        u"[2] foo",
    ]


def test_2_lines_together():
    marker_pattern = ur"\s*(?P<mark>\[\s*(?P<marknum>\d+)\s*\])"
    refs = [
        u"[1] hello",
        u"hello2 [2] foo",
    ]
    rebuilt_refs = rebuild_reference_lines(refs, marker_pattern)
    assert rebuilt_refs == [
        u"[1] hello hello2",
        u"[2] foo",
    ]


def test_get_number_header_lines_does_not_crash_on_final_empty_page(pdf_files):
    assert extract_references_from_file(pdf_files[4])
