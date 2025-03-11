import json

import mock
import pytest


def test_extract_journal_info(app_client):
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

    payload = {
        "journal_kb_data": journal_kb_data,
        "publication_infos": publication_infos,
    }

    headers = {
        "content-type": "application/json",
    }
    response = app_client.post(
        "/extract_journal_info",
        headers=headers,
        data=json.dumps(payload),
    )
    assert response.status_code == 200
    assert "extracted_publication_infos" in response.json
    assert len(response.json["extracted_publication_infos"]) == 2


@mock.patch(
    "refextract.app.extract_journal_reference", side_effect=KeyError("test message")
)
def test_extract_journal_info_when_timeout_from_refextract(
    mock_extract_refs, app_client
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

    payload = {
        "journal_kb_data": journal_kb_data,
        "publication_infos": publication_infos,
    }

    headers = {
        "content-type": "application/json",
    }
    response = app_client.post(
        "/extract_journal_info",
        headers=headers,
        data=json.dumps(payload),
    )
    assert response.status_code == 500
    assert response.json == {
        "message": "Can not extract publication info data. Reason: 'test message'"
    }


def test_extract_journal_info_for_multiple_pubinfos(app_client):
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

    payload = {
        "journal_kb_data": journal_kb_data,
        "publication_infos": publication_infos,
    }

    headers = {
        "content-type": "application/json",
    }
    response = app_client.post(
        "/extract_journal_info",
        headers=headers,
        data=json.dumps(payload),
    )
    assert response.status_code == 200
    assert "extracted_publication_infos" in response.json
    assert len(response.json["extracted_publication_infos"]) == 2


def test_extract_extract_references_from_text(app_client):
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
    }
    headers = {
        "content-type": "application/json",
    }
    text = "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581"
    payload = {"journal_kb_data": journal_kb_data, "text": text}
    response = app_client.post(
        "/extract_references_from_text",
        headers=headers,
        data=json.dumps(payload),
    )
    assert response.status_code == 200
    assert "extracted_references" in response.json
    assert len(response.json["extracted_references"]) == 1
    assert "author" in response.json["extracted_references"][0]
    assert "misc" in response.json["extracted_references"][0]
    assert "year" in response.json["extracted_references"][0]


@mock.patch(
    "refextract.app.extract_references_from_string",
    side_effect=KeyError("test message"),
)
def test_extract_references_from_text_when_timeout_from_refextract(
    mock_extract_refs, app_client
):
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
    }
    headers = {
        "content-type": "application/json",
    }
    text = "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581"
    payload = {"journal_kb_data": journal_kb_data, "text": text}
    response = app_client.post(
        "/extract_references_from_text", headers=headers, data=json.dumps(payload)
    )
    assert response.status_code == 500
    assert response.json == {
        "message": "Can not extract references. Reason: 'test message'"
    }


def test_extract_extract_references_from_list(app_client):
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
    }
    headers = {
        "content-type": "application/json",
    }
    raw_references = [
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581",
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 582",
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 583",
    ]
    payload = {"journal_kb_data": journal_kb_data, "raw_references": raw_references}
    response = app_client.post(
        "/extract_references_from_list",
        headers=headers,
        data=json.dumps(payload),
    )
    assert response.status_code == 200
    assert "extracted_references" in response.json
    assert len(response.json["extracted_references"]) == 3
    for reference in response.json["extracted_references"]:
        assert "author" in reference
        assert "misc" in reference
        assert "year" in reference


@mock.patch(
    "refextract.app.extract_references_from_string",
    side_effect=KeyError("test message"),
)
def test_extract_extract_references_from_list_when_error_from_refextract(
    mock_extract_refs, app_client
):
    journal_kb_data = {
        "COMMUNICATIONS IN ASTEROSEISMOLOGY": "Commun.Asteros.",
        "PHYS REV": "Phys.Rev.",
        "PHYSICAL REVIEW": "Phys.Rev.",
    }
    headers = {
        "content-type": "application/json",
    }
    raw_references = [
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581",
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 582",
        "Iskra Ł W et al 2017 Acta Phys. Pol. B 48 583",
    ]
    payload = {"journal_kb_data": journal_kb_data, "raw_references": raw_references}
    response = app_client.post(
        "/extract_references_from_list",
        headers=headers,
        data=json.dumps(payload),
    )

    expected_response = [
        {"raw_ref": ["Iskra Ł W et al 2017 Acta Phys. Pol. B 48 581"]},
        {"raw_ref": ["Iskra Ł W et al 2017 Acta Phys. Pol. B 48 582"]},
        {"raw_ref": ["Iskra Ł W et al 2017 Acta Phys. Pol. B 48 583"]},
    ]
    assert response.status_code == 200
    assert response.json["extracted_references"] == expected_response


@pytest.mark.vcr
def test_extract_extract_references_from_url(app_client):
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
    headers = {
        "content-type": "application/json",
    }
    url = "https://inspirehep.net/files/33ea6e86a7bfb4cab4734ed5c14d4529"
    payload = {"url": url, "journal_kb_data": journal_kb_data}
    response = app_client.post(
        "/extract_references_from_url",
        headers=headers,
        data=json.dumps(payload),
    )
    assert response.status_code == 200
    assert "extracted_references" in response.json
    assert len(response.json["extracted_references"]) == 2
