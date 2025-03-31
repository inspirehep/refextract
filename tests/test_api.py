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

import pytest
import responses

from refextract.references.api import (
    extract_journal_reference,
    extract_references_from_file,
    extract_references_from_string,
    extract_references_from_url,
)
from refextract.references.errors import FullTextNotAvailableError


@pytest.fixture
def kbs_override():
    return {
        "books": [("Griffiths, David", "Introduction to elementary particles", "2008")],
        "journals": [
            (
                "PHYSICAL REVIEW SPECIAL TOPICS ACCELERATORS AND BEAMS",
                "Phys.Rev.ST Accel.Beams",
            ),
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
            (
                "SITZUNGSBER PREUSS AKAD WISS PHYS MATH KL",
                "Sitzungsber.Preuss.Akad.Wiss.Berlin (Math.Phys.)",
            ),
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
        "journals_re": [
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
        ],
    }


def test_journal_extract():
    r = extract_journal_reference("Science Vol. 338 no. 6108 (2012) pp. 773-775")
    assert r["year"] == "2012"
    assert r["volume"] == "338"
    assert r["page"] == "773-775"
    assert r["title"] == "Science"


def test_extract_references_from_string(kbs_override):
    ref_lines = """[9] R. Bousso, JHEP 9906:028 (1999); hep-th/9906022."""
    r = extract_references_from_string(ref_lines, override_kbs_files=kbs_override)
    assert len(r) == 2


def test_extract_references_from_file(pdf_files):
    pdf = pdf_files["1503.07589v1.pdf"]
    r = extract_references_from_file(pdf)
    assert "texkey" in r[0]
    assert "author" in r[0]
    assert "url" in r[0]
    assert len(r) == 36
    with pytest.raises(FullTextNotAvailableError):
        extract_references_from_file(pdf + "error")


def test_extract_references_from_file_dois_as_pdfs_annotations(pdf_files):
    """Test DOIs as PDFs annotations and texkeys as named destinations"""
    pdf_file_with_dois_as_pdfs_annotations = pdf_files["2503.05372.pdf"]
    extracted_references = extract_references_from_file(
        pdf_file_with_dois_as_pdfs_annotations
    )
    first_reference = extracted_references[0]
    assert len(first_reference["url"]) == 2
    assert "https://doi.org/10.1103/PhysRevD.68.037502" in first_reference["url"]
    assert "texkey" in first_reference
    assert "Cahn:2003cw" in first_reference["texkey"]
    assert len(extracted_references) == 39


def test_extract_references_from_file_does_not_ignore_letters_in_volume(pdf_files):
    """Test that letters in volume are not ignored."""
    pdf = pdf_files["2503.05621.pdf"]
    extracted_references = extract_references_from_file(pdf)
    fith_reference = extracted_references[4]
    assert "journal_volume" in fith_reference
    assert fith_reference["journal_reference"][0] == "Phys. Rev. D95 (2017) 114510"
    assert fith_reference["journal_volume"][0] == "D95"
    assert len(extracted_references) == 24


def test_extract_references_with_authors_after_references(pdf_files):
    """Test that references extracted even with authors after references."""
    pdf = pdf_files["2502.21088.pdf"]
    extracted_references = extract_references_from_file(pdf)
    first_reference = extracted_references[0]
    last_reference = extracted_references[-1]
    # assert first reference is correctly extracted
    assert first_reference["journal_reference"][0] == "Phys. Rev. Lett. 25 (1970) 316"
    assert first_reference["author"][0] == "S. D. Drell and T.-M. Yan"
    # assert last reference correctly extracts collaboration
    assert last_reference["collaboration"][0] == "ATLAS Collaboration"
    assert len(extracted_references) == 104


@pytest.mark.xfail(
    reason="It should not put an Author in author field as it is a collaboration. "
    "This happens because there are authors after the references."
)
def test_collaboration_without_author_when_authors_after_references(pdf_files):
    """Test that references extracted even with authors after references."""
    pdf = pdf_files["2502.21088.pdf"]
    extracted_references = extract_references_from_file(pdf)
    last_reference = extracted_references[-1]
    # assert last reference is correctly extracted
    assert last_reference["collaboration"][0] == "ATLAS Collaboration"
    assert "author" not in last_reference


@pytest.mark.xfail(
    reason="It should extract the journal reference and urls correctly."
)
def test_extract_references_two_column_layout(pdf_files):
    """Test that references extracted even with authors after references."""
    pdf = pdf_files["2502.18907.pdf"]
    extracted_references = extract_references_from_file(pdf)
    first_reference = extracted_references[0]
    assert (
        first_reference["author"][0]
        == "Adamopoulos G., Robertson J., Morrison N. A., Godet C."
    )
    assert first_reference["journal_reference"][0] == " J. Appl. Phys. 96 (2004) 6348"
    assert "url" in first_reference


def test_extract_references_with_multiple_refs_under_same_marker(pdf_files):
    """Test that references extracted even with authors after references."""
    pdf = pdf_files["2406.06875.pdf"]
    extracted_references = extract_references_from_file(pdf)
    first_reference = extracted_references[0]
    second_reference = extracted_references[1]
    third_reference = extracted_references[2]
    assert first_reference["author"][0] == "W.T. Tutte"
    assert second_reference["author"][0] == "W.T. Tutte"
    assert third_reference["author"][0] == "W.T. Tutte"
    assert first_reference["journal_reference"][0] == "Can. J. Math. 14 (1962) 21"
    assert second_reference["journal_reference"][0] == "Can. J. Math. 15 (1963) 249"
    assert (
        third_reference["journal_reference"][0] == "Bull. Am. Math. Soc. 74 (1968) 64"
    )
    assert first_reference["linemarker"][0] == "1"
    assert second_reference["linemarker"][0] == "1"
    assert third_reference["linemarker"][0] == "1"


@responses.activate
def test_extract_references_from_url(pdf_files):
    with open(pdf_files["1503.07589v1.pdf"], "rb") as fd:
        url = "http://arxiv.org/pdf/1503.07589v1.pdf"
        responses.add(
            responses.GET, url, body=fd.read(), content_type="application/pdf"
        )

    r = extract_references_from_url(url)
    assert len(r) == 36
    assert "url" in r[0]

    url = "http://www.example.com"
    responses.add(
        responses.GET,
        url,
        body="File not found!",
        status=404,
        content_type="text/plain",
    )
    with pytest.raises(FullTextNotAvailableError):
        extract_references_from_url(url)


def test_long_registrant_dois(pdf_files):
    """DOIs with 5 digit registrant code"""
    r = extract_references_from_file(pdf_files["wepml008.pdf"])
    assert len(r) == 6
    for ref in r[1:]:
        assert "doi" in ref
        assert ref.get("doi")[0].startswith("doi:10.18429/JACoW")


def test_override_kbs_files_can_take_journals_dict():
    journals = {"Journal of Testing": "J.Testing"}
    reference = "J. Smith, Journal of Testing 42 (2020) 1234"

    result = extract_references_from_string(
        reference, override_kbs_files={"journals": journals}
    )
    assert result[0]["journal_title"] == ["J.Testing"]
