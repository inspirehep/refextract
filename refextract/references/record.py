# -*- coding: utf-8 -*-
#
# This file is part of refextract.
# Copyright (C) 2013, 2015, 2016, 2017, 2018 CERN.
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


def format_marker(line_marker):
    return line_marker.strip("[](){}. ")


def build_references(citations, reference_format=False):
    """Build list of reference dictionaries from a references list
    """
    # Now, run the method which will take as input:
    # 1. A list of lists of dictionaries, where each dictionary is a piece
    # of citation information corresponding to a tag in the citation.
    # 2. The line marker for this entire citation line (mulitple citation
    # 'finds' inside a single citation will use the same marker value)
    # The resulting xml line will be a properly marked up form of the
    # citation. It will take into account authors to try and split up
    # references which should be read as two SEPARATE ones.
    return [c for citation_elements in citations
            for elements in citation_elements['elements']
            for c in build_reference_fields(elements,
                                            citation_elements['line_marker'],
                                            citation_elements['raw_ref'],
                                            reference_format)]


def add_subfield(field, code, value):
    if value:
        field.setdefault(code, []).append(value)


def add_journal_subfield(field, element, reference_format):
    add_subfield(field, 'journal_title', element.get('title'))
    add_subfield(field, 'journal_volume', element.get('volume'))
    add_subfield(field, 'journal_year', element.get('year'))
    add_subfield(field, 'journal_page', element.get('page'))
    add_subfield(field, 'journal_reference',
                 reference_format.format(**element))


def create_reference_field(line_marker):
    field = {}
    if line_marker.strip("., [](){}"):
        add_subfield(field, 'linemarker', format_marker(line_marker))
    return field


def build_reference_fields(citation_elements, line_marker, raw_ref,
                           reference_format):
    """Create the final representation of the reference information.

    @param citation_elements: (list) an ordered list of dictionary elements,
                              with each element corresponding to a found
                              piece of information from a reference line.
    @param line_marker: (string) The line marker for this single reference
                        line (e.g. [19])
    @param raw_ref: (string) The raw string of this line
    @return reference_fields: (list) A list of one dictionary containing the
                      reference elements
    """
    # Begin the datafield element
    current_field = create_reference_field(line_marker)
    current_field['raw_ref'] = [raw_ref]

    reference_fields = [current_field]

    for element in citation_elements:
        # Before going onto checking 'what' the next element is,
        # handle misc text and semi-colons
        # Multiple misc text subfields will be compressed later
        # This will also be the only part of the code that deals with MISC
        # tag_typed elements
        misc_txt = element['misc_txt']
        if misc_txt.strip("., [](){}"):
            misc_txt = misc_txt.lstrip('])} ,.').rstrip('[({ ,.')
            add_subfield(current_field, 'misc', misc_txt)

        # Now handle the type dependent actions
        # JOURNAL
        if element['type'] == "JOURNAL":
            add_journal_subfield(current_field, element, reference_format)

        # REPORT NUMBER
        elif element['type'] == "REPORTNUMBER":
            add_subfield(current_field, 'reportnumber', element['report_num'])

        # URL
        elif element['type'] == "URL":
            if element['url_string'] == element['url_desc']:
                # Build the datafield for the URL segment of the reference
                # line:
                add_subfield(current_field, 'url', element['url_string'])
            # Else, in the case that the url string and the description differ
            # in some way, include them both
            else:
                add_subfield(current_field, 'url', element['url_string'])
                add_subfield(current_field, 'urldesc', element['url_desc'])

        # DOI
        elif element['type'] == "DOI":
            add_subfield(current_field, 'doi', 'doi:' + element['doi_string'])

        # HDL
        elif element['type'] == "HDL":
            add_subfield(current_field, 'hdl', 'hdl:' + element['hdl_id'])

        # AUTHOR
        elif element['type'] == "AUTH":
            value = element['auth_txt']
            if element['auth_type'] == 'incl':
                value = "(%s)" % value

            add_subfield(current_field, 'author', value)

        elif element['type'] == "QUOTED":
            add_subfield(current_field, 'title', element['title'])

        elif element['type'] == "ISBN":
            add_subfield(current_field, 'isbn', element['ISBN'])

        elif element['type'] == "BOOK":
            add_subfield(current_field, 'title', element['title'])

        elif element['type'] == "PUBLISHER":
            add_subfield(current_field, 'publisher', element['publisher'])

        elif element['type'] == "YEAR":
            add_subfield(current_field, 'year', element['year'])

        elif element['type'] == "COLLABORATION":
            add_subfield(current_field,
                         'collaboration',
                         element['collaboration'])

        elif element['type'] == "RECID":
            add_subfield(current_field, 'recid', str(element['recid']))

    return reference_fields


def merge_misc(field):
    current_misc = None
    for subfield in field.subfields[:]:
        if subfield.code == 'm':
            if current_misc is None:
                current_misc = subfield
            else:
                current_misc.value += " " + subfield.value
                field.subfields.remove(subfield)
