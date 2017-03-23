# -*- coding: utf-8 -*-
#
# This file is part of refextract
# Copyright (C) 2016 CERN.
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

"""The Refextract unit test suite"""

import pytest

from refextract.references.engine import (
    get_plaintext_document_body,
    parse_references,
)

from refextract.references.errors import UnknownDocumentTypeError

from refextract.references.text import wash_and_repair_reference_line


def get_references(ref_line, override_kbs_files=None):
    return parse_references([ref_line], override_kbs_files=override_kbs_files)


def test_month_with_year():
    ref_line = u"""[2] S. Weinberg, A Model of Leptons, Phys. Rev. Lett. 19 (Nov, 1967) 1264–1266."""
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'S. Weinberg, A Model of Leptons'],
            'journal_page': [u'1264-1266'],
            'journal_reference': [u'Phys. Rev. Lett. 19 (1967) 1264-1266'],
            'journal_title': [u'Phys. Rev. Lett.'],
            'journal_volume': [u'19'],
            'journal_year': [u'1967'],
            'linemarker': [u'2'],
            'year': [u'1967'],
            'raw_ref': [ref_line],
        }
    ]
    assert references == expected


def test_numeration_not_finding_year():
    ref_line = u"""[137] M. Papakyriacou, H. Mayer, C. Pypen, H. P. Jr., and S. Stanzl-Tschegg, “Inﬂuence of loading frequency on high cycle fatigue properties of b.c.c. and h.c.p. metals,” Materials Science and Engineering, vol. A308, pp. 143–152, 2001."""
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'M. Papakyriacou, H. Mayer, C. Pypen, H. P. Jr., and S. Stanzl-Tschegg'],
            'journal_page': [u'143-152'],
            'journal_reference': [u'Mat.Sci.Eng. A308 (2001) 143-152'],
            'journal_title': [u'Mat.Sci.Eng.'],
            'journal_volume': [u'A308'],
            'journal_year': [u'2001'],
            'linemarker': [u'137'],
            'year': [u'2001'],
            'title': [u'Influence of loading frequency on high cycle fatigue properties of b.c.c. and h.c.p. metals'],
            'raw_ref': [ref_line],
        }
    ]
    assert references == expected


def test_numeration_not_finding_year2():
    ref_line = u"""[138] Y.-B. Park, R. Mnig, and C. A. Volkert, “Frequency effect on thermal fatigue damage in Cu interconnects,” Thin Solid Films, vol. 515, pp. 3253– 3258, 2007."""
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'Y.-B. Park, R. Mnig, and C. A. Volkert'],
            'journal_page': [u'3253-3258'],
            'journal_reference': [u'Thin Solid Films 515 (2007) 3253-3258'],
            'journal_title': [u'Thin Solid Films'],
            'journal_volume': [u'515'],
            'journal_year': [u'2007'],
            'linemarker': [u'138'],
            'year': [u'2007'],
            'title': [u'Frequency effect on thermal fatigue damage in Cu interconnects'],
            'raw_ref': [ref_line],
        }
    ]
    assert references == expected


def test_extra_a_in_report_number():
    ref_line = u'[14] CMS Collaboration, CMS-PAS-HIG-12-002. CMS Collaboration, CMS-PAS-HIG-12-008. CMS Collaboration, CMS-PAS-HIG-12-022. ATLAS Collaboration, arXiv:1205.0701. ATLAS Collaboration, ATLAS-CONF-2012-078.'
    res = get_references(ref_line)
    references = res[0]
    assert len(references) == 1
    assert references[0]['collaboration'] == [
        u'CMS Collaboration',
        u'ATLAS Collaboration',
    ]
    assert references[0]['reportnumber'] == [
        u'CMS-PAS-HIG-12-002',
        u'CMS-PAS-HIG-12-008',
        u'CMS-PAS-HIG-12-022',
        u'arXiv:1205.0701',
        u'ATLAS-CONF-2012-078',
    ]
    assert references[0]['linemarker'] == [u'14']


def test_get_plaintext_document_body(tmpdir):
    input = [u"Some text\n", u"on multiple lines\n"]
    f = tmpdir.join("plain.txt")
    f.write("".join(input))
    assert input == get_plaintext_document_body(str(f))

    with pytest.raises(UnknownDocumentTypeError) as excinfo:
        html = "<html><body>Some page</body></html>"
        f = tmpdir.join("page.html")
        f.write(html)
        get_plaintext_document_body(str(f))
    assert 'text/html' in excinfo.value
