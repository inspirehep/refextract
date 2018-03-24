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

import pytest
import responses

from refextract.references.api import (
    extract_journal_reference,
    extract_references_from_string,
    extract_references_from_url,
    extract_references_from_file,
)

from refextract.references.errors import FullTextNotAvailableError


@pytest.fixture
def kbs_override():
    return {
        "books": [
            ('Griffiths, David', 'Introduction to elementary particles', '2008')
        ],
        "journals": [
            ("PHYSICAL REVIEW SPECIAL TOPICS ACCELERATORS AND BEAMS", "Phys.Rev.ST Accel.Beams"),
            ("PHYS REV D", "Phys.Rev.;D"),
            ("PHYS REV", "Phys.Rev."),
            ("PHYS REV LETT", "Phys.Rev.Lett."),
            ("PHYS LETT", "Phys.Lett."),
            ("J PHYS", "J.Phys."),
            ("JOURNAL OF PHYSICS", "J.Phys."),
            ("J PHYS G", "J.Phys.;G"),
            ("PHYSICAL REVIEW", "Phys.Rev."),
            ("ADV THEO MATH PHYS", "Adv.Theor.Math.Phys."),
            ("MATH PHYS", "Math.Phys."),
            ("J MATH PHYS", "J.Math.Phys."),
            ("JHEP", "JHEP"),
            ("SITZUNGSBER PREUSS AKAD WISS PHYS MATH KL", "Sitzungsber.Preuss.Akad.Wiss.Berlin (Math.Phys.)"),
            ("PHYS LETT", "Phys.Lett."),
            ("NUCL PHYS", "Nucl.Phys."),
            ("NUCL PHYS", "Nucl.Phys."),
            ("NUCL PHYS PROC SUPPL", "Nucl.Phys.Proc.Suppl."),
            ("JINST", "JINST"),
            ("THE EUROPEAN PHYSICAL JOURNAL C PARTICLES AND FIELDS", "Eur.Phys.J.;C"),
            ("COMMUN MATH PHYS", "Commun.Math.Phys."),
            ("COMM MATH PHYS", "Commun.Math.Phys."),
            ("REV MOD PHYS", "Rev.Mod.Phys."),
            ("ANN PHYS U S", "Ann.Phys."),
            ("AM J PHYS", "Am.J.Phys."),
            ("PROC R SOC LONDON SER", "Proc.Roy.Soc.Lond."),
            ("CLASS QUANT GRAVITY", "Class.Quant.Grav."),
            ("FOUND PHYS", "Found.Phys."),
            ("IEEE TRANS NUCL SCI", "IEEE Trans.Nucl.Sci."),
            ("SCIENCE", "Science"),
            ("ACTA MATERIALIA", "Acta Mater."),
            ("REVIEWS OF MODERN PHYSICS", "Rev.Mod.Phys."),
            ("NUCL INSTRUM METHODS", "Nucl.Instrum.Meth."),
            ("Z PHYS", "Z.Phys."),
        ],
        "journals-re": [
            "DAN---Dokl.Akad.Nauk Ser.Fiz.",
        ],
        "report-numbers": [
            "#####CERN#####",
            "< yy 999>",
            "< yyyy 999>",
            "ATL CONF---ATL-CONF",
            "ATL PHYS INT---ATL-PHYS-INT",
            "ATLAS CONF---ATL-CONF",
            "#####LANL#####",
            "<s/syymm999>",
            "<syymm999>",
            "ASTRO PH---astro-ph",
            "HEP PH---hep-ph",
            "HEP TH---hep-th",
            "HEP EX---hep-ex",
            "#####LHC#####",
            "< yy 999>",
            "<syyyy 999>",
            "< 999>",
            "< 9999>",
            "CERN LHC PROJECT REPORT---CERN-LHC-Project-Report",
            "CLIC NOTE              ---CERN-CLIC-Note",
            "CERN LHCC              ---CERN-LHCC",
            "CERN EP                ---CERN-EP",
            "######ATLANTIS#######",
            "< 9999999>",
            "CERN EX---CERN-EX",
        ]
    }


def test_journal_extract():
    r = extract_journal_reference("Science Vol. 338 no. 6108 (2012) pp. 773-775")
    assert r['year'] == u'2012'
    assert r['volume'] == u'338'
    assert r['page'] == u'773-775'
    assert r['title'] == u'Science'


def test_extract_references_from_string(kbs_override):
    ref_lines = """[9] R. Bousso, JHEP 9906:028 (1999); hep-th/9906022."""
    r = extract_references_from_string(ref_lines, override_kbs_files=kbs_override)
    assert len(r) == 2


def test_extract_references_from_file(pdf_files):
    r = extract_references_from_file(pdf_files[0])
    assert 'texkey' in r[0]
    assert 'author' in r[0]
    assert len(r) == 36
    with pytest.raises(FullTextNotAvailableError):
        extract_references_from_file(pdf_files[0] + "error")


@responses.activate
def test_extract_references_from_url(pdf_files):
    with open(pdf_files[0], 'rb') as fd:
        url = "http://arxiv.org/pdf/1503.07589v1.pdf"
        responses.add(
            responses.GET,
            url,
            body=fd.read(),
            content_type='application/pdf'
        )

    r = extract_references_from_url(url)
    assert len(r) == 36

    with pytest.raises(FullTextNotAvailableError):
        url = "http://www.example.com"
        responses.add(
            responses.GET,
            url,
            body="File not found!",
            status=404,
            content_type='text/plain',
        )
        extract_references_from_url(url)
