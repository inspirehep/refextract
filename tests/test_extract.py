import mock
import pytest

from refextract.extract import (
    extract_journal_info,
    extract_references_from_file_url,
    extract_references_from_list,
    extract_references_from_text,
)


def test_extract_journal_info():
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
        "PHYS REV LETT": "Phys.Rev.Lett.",
        "JINST": "JINST",
        "JOURNAL OF INSTRUMENTATION": "JINST",
        "SENS ACTUATORS B": "Sens.Actuators B",
        "SENSORS AND ACTUATORS B: CHEMICAL": "Sens.Actuators B",
        "PHYS SCRIPTA": "Phys.Scripta",
        "PHYSICA SCRIPTA": "Phys.Scripta",
        "BULL CALCUTTA MATH SOC": "Bull.Calcutta Math.Soc.",
        "BULLETIN OF THE CALCUTTA MATHEMATICAL SOCIETY": "Bull.Calcutta Math.Soc.",
        "QUANTUM MACHINE INTELLIGENCE": "Quantum Machine Intelligence",
    }
    publication_infos = [
        {"pubinfo_freetext": "Phys. Rev. 127 (1962) 965-970"},
        {"journal_title": "Phys. Rev."},
    ]

    extracted = extract_journal_info(publication_infos, journal_kb_data)

    assert "extracted_publication_infos" in extracted
    assert len(extracted["extracted_publication_infos"]) == 2


@mock.patch("refextract.extract.extract_journal_reference", side_effect=KeyError)
def test_extract_journal_info_when_timeout_from_refextract(
    extract_journal_reference_mock,
):
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
        "PHYS REV LETT": "Phys.Rev.Lett.",
        "JINST": "JINST",
        "JOURNAL OF INSTRUMENTATION": "JINST",
        "SENS ACTUATORS B": "Sens.Actuators B",
        "SENSORS AND ACTUATORS B: CHEMICAL": "Sens.Actuators B",
        "PHYS SCRIPTA": "Phys.Scripta",
        "PHYSICA SCRIPTA": "Phys.Scripta",
        "BULL CALCUTTA MATH SOC": "Bull.Calcutta Math.Soc.",
        "BULLETIN OF THE CALCUTTA MATHEMATICAL SOCIETY": "Bull.Calcutta Math.Soc.",
        "QUANTUM MACHINE INTELLIGENCE": "Quantum Machine Intelligence",
    }
    publication_infos = [{"pubinfo_freetext": "Phys. Rev. 127 (1962) 965-970"}]

    extracted = extract_journal_info(publication_infos, journal_kb_data)

    assert not extracted


def test_extract_journal_info_for_multiple_pubinfos():
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
        "PHYS REV LETT": "Phys.Rev.Lett.",
        "JINST": "JINST",
        "JOURNAL OF INSTRUMENTATION": "JINST",
        "SENS ACTUATORS B": "Sens.Actuators B",
        "SENSORS AND ACTUATORS B: CHEMICAL": "Sens.Actuators B",
        "PHYS SCRIPTA": "Phys.Scripta",
        "PHYSICA SCRIPTA": "Phys.Scripta",
        "BULL CALCUTTA MATH SOC": "Bull.Calcutta Math.Soc.",
        "BULLETIN OF THE CALCUTTA MATHEMATICAL SOCIETY": "Bull.Calcutta Math.Soc.",
        "QUANTUM MACHINE INTELLIGENCE": "Quantum Machine Intelligence",
    }
    publication_infos = [
        {"pubinfo_freetext": "Phys. Rev. 127 (1962) 965-970"},
        {"pubinfo_freetext": "Phys.Rev.Lett. 127 (1962) 965-970"},
    ]

    extracted = extract_journal_info(publication_infos, journal_kb_data)

    assert "extracted_publication_infos" in extracted
    assert len(extracted["extracted_publication_infos"]) == 2


def test_extract_extract_references_from_text():
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
    }
    text = "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581"

    extracted = extract_references_from_text(text, journal_kb_data)

    assert "extracted_references" in extracted
    assert len(extracted["extracted_references"]) == 1
    assert "author" in extracted["extracted_references"][0]
    assert "misc" in extracted["extracted_references"][0]
    assert "year" in extracted["extracted_references"][0]


@mock.patch("refextract.extract.extract_references_from_string", side_effect=KeyError)
def test_extract_references_from_text_when_timeout_from_refextract(
    extract_references_from_string_mock,
):
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
    }

    text = "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581"

    extracted = extract_references_from_text(text, journal_kb_data)

    assert not extracted


def test_extract_references_from_list():
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
    }
    raw_references = [
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581",
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 582",
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 583",
    ]

    extracted = extract_references_from_list(raw_references, journal_kb_data)

    assert "extracted_references" in extracted
    assert len(extracted["extracted_references"]) == 3
    for reference in extracted["extracted_references"]:
        assert "author" in reference
        assert "misc" in reference
        assert "year" in reference


@mock.patch("refextract.extract.extract_references_from_string", side_effect=KeyError)
def test_extract_references_from_list_when_error_from_refextract(
    extract_references_from_string_mock,
):
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
    }
    raw_references = [
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581",
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 582",
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 583",
    ]

    extracted = extract_references_from_list(raw_references, journal_kb_data)

    expected_response = [
        {"raw_ref": ["Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581"]},
        {"raw_ref": ["Iskra Ł W et al 2017 Acta Phys. Pol. B 48 582"]},
        {"raw_ref": ["Iskra Ł W et al 2017 Acta Phys. Pol. B 48 583"]},
    ]
    assert extracted["extracted_references"] == expected_response


@pytest.mark.vcr
def test_extract_references_from_url():
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
        "PHYS REV LETT": "Phys.Rev.Lett.",
        "JINST": "JINST",
        "JOURNAL OF INSTRUMENTATION": "JINST",
        "SENS ACTUATORS B": "Sens.Actuators B",
        "SENSORS AND ACTUATORS B: CHEMICAL": "Sens.Actuators B",
        "PHYS SCRIPTA": "Phys.Scripta",
        "PHYSICA SCRIPTA": "Phys.Scripta",
        "BULL CALCUTTA MATH SOC": "Bull.Calcutta Math.Soc.",
        "BULLETIN OF THE CALCUTTA MATHEMATICAL SOCIETY": "Bull.Calcutta Math.Soc.",
        "QUANTUM MACHINE INTELLIGENCE": "Quantum Machine Intelligence",
    }
    url = "https://inspirehep.net/files/33ea6e86a7bfb4cab4734ed5c14d4529"

    extracted = extract_references_from_file_url(url, journal_kb_data)

    assert "extracted_references" in extracted
    assert len(extracted["extracted_references"]) == 2
