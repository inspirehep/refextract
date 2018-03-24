# -*- coding: utf-8 -*-
#
# This file is part of refextract.
# Copyright (C) 2013, 2015, 2016, 2018 CERN.
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

"""This is where all the public API calls are accessible to extract references.

There are 4 API functions available to extract from PDF file, string or URL. In
addition, there is an API call to return a parsed journal reference structure
from a raw string.
"""

from __future__ import absolute_import, division, print_function

import os
import sys
import requests
import magic

from tempfile import mkstemp
from itertools import izip

from .engine import (
    get_kbs,
    get_plaintext_document_body,
    parse_reference_line,
    parse_references,
)
from .errors import FullTextNotAvailableError
from .find import (find_numeration_in_body,
                   get_reference_section_beginning)
from .pdf import extract_texkeys_from_pdf
from .text import extract_references_from_fulltext, rebuild_reference_lines


def extract_references_from_url(url, headers=None, chunk_size=1024, **kwargs):
    """Extract references from the pdf specified in the url.

    The first parameter is the URL of the file.
    It returns a list of parsed references.

    It raises FullTextNotAvailableError if the URL gives a 404,
    UnknownDocumentTypeError if it is not a PDF or plain text.

    The standard reference format is: {title} {volume} ({year}) {page}.

    E.g. you can change that by passing the reference_format:

    >>> extract_references_from_url(path, reference_format="{title},{volume},{page}")

    If you want to also link each reference to some other resource (like a record),
    you can provide a linker_callback function to be executed for every reference
    element found.

    To override KBs for journal names etc., use ``override_kbs_files``:

    >>> extract_references_from_url(path, override_kbs_files={'journals': 'my/path/to.kb'})

    """
    # Get temporary filepath to download to
    filename, filepath = mkstemp(
        suffix=u"_{0}".format(os.path.basename(url)),
    )
    os.close(filename)

    try:
        req = requests.get(
            url=url,
            headers=headers,
            stream=True
        )
        req.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in req.iter_content(chunk_size):
                f.write(chunk)
        references = extract_references_from_file(filepath, **kwargs)
    except requests.exceptions.HTTPError:
        raise FullTextNotAvailableError(u"URL not found: '{0}'".format(url)), None, sys.exc_info()[2]
    finally:
        os.remove(filepath)
    return references


def extract_references_from_file(path,
                                 recid=None,
                                 reference_format=u"{title} {volume} ({year}) {page}",
                                 linker_callback=None,
                                 override_kbs_files=None):
    """Extract references from a local pdf file.

    The first parameter is the path to the file.
    It returns a list of parsed references.
    It raises FullTextNotAvailableError if the file does not exist,
    UnknownDocumentTypeError if it is not a PDF or plain text.

    The standard reference format is: {title} {volume} ({year}) {page}.

    E.g. you can change that by passing the reference_format:

    >>> extract_references_from_file(path, reference_format=u"{title},{volume},{page}")

    If you want to also link each reference to some other resource (like a record),
    you can provide a linker_callback function to be executed for every reference
    element found.

    To override KBs for journal names etc., use ``override_kbs_files``:

    >>> extract_references_from_file(path, override_kbs_files={'journals': 'my/path/to.kb'})

    """
    if not os.path.isfile(path):
        raise FullTextNotAvailableError(u"File not found: '{0}'".format(path))

    docbody = get_plaintext_document_body(path)
    reflines, dummy, dummy = extract_references_from_fulltext(docbody)
    if not reflines:
        docbody = get_plaintext_document_body(path, keep_layout=True)
        reflines, dummy, dummy = extract_references_from_fulltext(docbody)

    parsed_refs, stats = parse_references(
        reflines,
        recid=recid,
        reference_format=reference_format,
        linker_callback=linker_callback,
        override_kbs_files=override_kbs_files,
    )

    if magic.from_file(path, mime=True) == "application/pdf":
        texkeys = extract_texkeys_from_pdf(path)
        if len(texkeys) == len(parsed_refs):
            parsed_refs = [dict(ref, texkey=[key]) for ref, key in izip(parsed_refs, texkeys)]

    return parsed_refs


def extract_references_from_string(source,
                                   is_only_references=True,
                                   recid=None,
                                   reference_format="{title} {volume} ({year}) {page}",
                                   linker_callback=None,
                                   override_kbs_files=None):
    """Extract references from a raw string.

    The first parameter is the path to the file.
    It returns a tuple (references, stats).

    If the string does not only contain references, improve accuracy by
    specifing ``is_only_references=False``.

    The standard reference format is: {title} {volume} ({year}) {page}.

    E.g. you can change that by passing the reference_format:

    >>> extract_references_from_string(path, reference_format="{title},{volume},{page}")

    If you want to also link each reference to some other resource (like a record),
    you can provide a linker_callback function to be executed for every reference
    element found.

    To override KBs for journal names etc., use ``override_kbs_files``:

    >>> extract_references_from_string(path, override_kbs_files={'journals': 'my/path/to.kb'})
    """
    docbody = source.split('\n')
    if not is_only_references:
        reflines, dummy, dummy = extract_references_from_fulltext(docbody)
    else:
        refs_info = get_reference_section_beginning(docbody)
        if not refs_info:
            refs_info, dummy = find_numeration_in_body(docbody)
            refs_info['start_line'] = 0
            refs_info['end_line'] = len(docbody) - 1,

        reflines = rebuild_reference_lines(
            docbody, refs_info['marker_pattern'])
    parsed_refs, stats = parse_references(
        reflines,
        recid=recid,
        reference_format=reference_format,
        linker_callback=linker_callback,
        override_kbs_files=override_kbs_files,
    )
    return parsed_refs


def extract_journal_reference(line, override_kbs_files=None):
    """Extract the journal reference from string.

    Extracts the journal reference from string and parses for specific
    journal information.
    """
    kbs = get_kbs(custom_kbs_files=override_kbs_files)
    references, dummy_m, dummy_c, dummy_co = parse_reference_line(line, kbs)

    for elements in references:
        for el in elements:
            if el['type'] == 'JOURNAL':
                return el
