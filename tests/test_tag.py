# -*- coding: utf-8 -*-
#
# This file is part of refextract
# Copyright (C) 2016, 2018, 2020 CERN.
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

from refextract.references.tag import (
    find_numeration,
    find_numeration_more,
    identify_ibids,
    tag_arxiv,
)


def test_vol_page_year():
    "<vol>, <page> (<year>)"
    ref_line = u"""24, 418 (1930)"""
    r = find_numeration(ref_line)
    assert r['volume'] == u"24"
    assert r['year'] == u"1930"
    assert r['page'] == u"418"


def test_vol_year_page():
    "<vol>, (<year>) <page> "
    ref_line = u"""24, (1930) 418"""
    r = find_numeration(ref_line)
    assert r['volume'] == u"24"
    assert r['year'] == u"1930"
    assert r['page'] == u"418"


def test_year_title_volume_page():
    "<year>, <title> <vol> <page> "
    ref_line = u"""1930 <cds.JOURNAL>J.Phys.</cds.JOURNAL> 24, 418"""
    r = find_numeration_more(ref_line)
    assert r['volume'] == u"24"
    assert r['year'] == u"1930"
    assert r['page'] == u"418"


def test_identify_ibids_empty():
    r = identify_ibids("")
    assert r == ({}, '')


def test_identify_ibids_simple():
    ref_line = u"""[46] E. Schrodinger, Sitzungsber. Preuss. Akad. Wiss. Phys. Math.
    Kl. 24, 418(1930); ibid, 3, 1(1931)"""
    r = identify_ibids(ref_line.upper())
    assert r == ({85: u'IBID'}, u'[46] E. SCHRODINGER, SITZUNGSBER. PREUSS. AKAD. '
                                u'WISS. PHYS. MATH. KL. 24, 418(1930); ____, 3, '
                                u'1(1931)')


def test_4_digits():
    ref_line = u"""{any prefix}arXiv:1003.1111{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1003.1111</cds.ARXIV>{any "
                             u"postfix}")


def test_4_digits_suffix():
    ref_line = u"""{any prefix}arXiv:1104.2222 [physics.ins-det]{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1104.2222 ["
                             u"physics.ins-det]</cds.ARXIV>{any postfix}")


def test_5_digits():
    ref_line = u"""{any prefix}arXiv:1303.33333{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1303.33333</cds.ARXIV>{any "
                             u"postfix}")


def test_5_digits_2012():
    ref_line = u"""{any prefix}arXiv:1203.33333{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == u"{any prefix}arXiv:1203.33333{any postfix}"


def test_5_digits_suffix():
    ref_line = u"""{any prefix}arXiv:1304.44444 [physics.ins-det]{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1304.44444 ["
                             u"physics.ins-det]</cds.ARXIV>{any postfix}")


def test_4_digits_version():
    ref_line = u"""{any prefix}arXiv:1003.1111v9{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1003.1111</cds.ARXIV>{any "
                             u"postfix}")


def test_4_digits_suffix_version():
    ref_line = u"""{any prefix}arXiv:1104.2222v9 [physics.ins-det]{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1104.2222 ["
                             u"physics.ins-det]</cds.ARXIV>{any postfix}")


def test_5_digits_version():
    ref_line = u"""{any prefix}arXiv:1303.33333v9{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1303.33333</cds.ARXIV>{any "
                             u"postfix}")


def test_5_digits_suffix_version():
    ref_line = u"""{any prefix}arXiv:1304.44444v9 [physics.ins-det]{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1304.44444 ["
                             u"physics.ins-det]</cds.ARXIV>{any postfix}")


def test_4_digits_new():
    ref_line = u"""{any prefix}9910.1234{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:9910.1234</cds.ARXIV>{any "
                             u"postfix}")


def test_4_digits_suffix_new():
    ref_line = u"""{any prefix}9910.1234 [physics.ins-det]{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:9910.1234 ["
                             u"physics.ins-det]</cds.ARXIV>{any postfix}")


def test_5_digits_new():
    ref_line = u"""{any prefix}1310.12345{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1310.12345</cds.ARXIV>{any "
                             u"postfix}")


def test_5_digits_suffix_new():
    ref_line = u"""{any prefix}1310.12345 [physics.ins-det]{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1310.12345 ["
                             u"physics.ins-det]</cds.ARXIV>{any postfix}")


def test_4_digits_version_new():
    ref_line = u"""{any prefix}9910.1234v9{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:9910.1234</cds.ARXIV>{any "
                             u"postfix}")


def test_4_digits_suffix_version_new():
    ref_line = u"""{any prefix}9910.1234v9 [physics.ins-det]{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:9910.1234 ["
                             u"physics.ins-det]</cds.ARXIV>{any postfix}")


def test_5_digits_version_new():
    ref_line = u"""{any prefix}1310.12345v9{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1310.12345</cds.ARXIV>{any "
                             u"postfix}")


def test_5_digits_suffix_version_new():
    ref_line = u"""{any prefix}1310.12345v9 [physics.ins-det]{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == (u"{any prefix}<cds.ARXIV>arXiv:1310.12345 ",
                             "[physics.ins-det]</cds.ARXIV>{any postfix}")


def test_5_digits_suffix_version_new_2012():
    ref_line = u"""{any prefix}1210.12345v9 [physics.ins-det]{any postfix}"""
    r = tag_arxiv(ref_line)
    assert r.strip(': ') == u"{any prefix}1210.12345v9 [physics.ins-det]{any postfix}"
