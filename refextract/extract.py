import logging

from refextract.references.api import (
    extract_journal_reference,
    extract_references_from_string,
    extract_references_from_url,
)

LOGGER = logging.getLogger(__name__)


def extract_journal_info(publication_infos, journal_kb_data):
    extracted_publication_infos = []
    journal_dict = {"journals": journal_kb_data}
    try:
        for publication_info in publication_infos:
            if not publication_info.get("pubinfo_freetext"):
                extracted_publication_infos.append({})
                continue
            extracted_publication_info = extract_journal_reference(
                publication_info["pubinfo_freetext"],
                override_kbs_files=journal_dict,
            )
            if not extracted_publication_info:
                extracted_publication_info = {}
            extracted_publication_infos.append(extracted_publication_info)
    except Exception as e:
        LOGGER.error(f"Failed to extract publication info data. Reason: {str(e)}")
        return None
    return {"extracted_publication_infos": extracted_publication_infos}


def extract_references_from_text(text, journal_kb_data):
    journal_dict = {"journals": journal_kb_data}
    try:
        extracted_references = extract_references_from_string(
            text,
            override_kbs_files=journal_dict,
            reference_format="{title},{volume},{page}",
        )
    except Exception as e:
        LOGGER.error(f"an not extract references. Reason: {str(e)}")
        return None
    return {"extracted_references": extracted_references}


def extract_references_from_file_url(url, journal_kb_data):
    journal_dict = {"journals": journal_kb_data}
    try:
        extracted_references = extract_references_from_url(
            url,
            **{
                "override_kbs_files": journal_dict,
                "reference_format": "{title},{volume},{page}",
            },
        )
    except Exception as e:
        LOGGER.error(f"Can not extract references. Reason: {str(e)}")
        return None
    return {"extracted_references": extracted_references}


def extract_references_from_list(raw_references, journal_kb_data):
    journal_dict = {"journals": journal_kb_data}
    extracted_references = []
    for reference in raw_references:
        try:
            extracted_reference = extract_references_from_string(
                reference,
                override_kbs_files=journal_dict,
                reference_format="{title},{volume},{page}",
            )
            if extracted_reference:
                extracted_references.append(extracted_reference[0])
            else:
                extracted_references.append({"raw_ref": [reference]})
        except Exception as e:
            LOGGER.error(f"Failed to extract reference: {reference}. Reason: {str(e)}")
            extracted_references.append({"raw_ref": [reference]})
    return {"extracted_references": extracted_references}
