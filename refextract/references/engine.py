# -*- coding: utf-8 -*-
#
# This file is part of refextract.
# Copyright (C) 2013, 2015, 2016, 2017, 2018, 2020 CERN.
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

"""Main engine responsible for extracting references from PDF documents."""

import logging
import mmap
import re
from datetime import datetime

import magic

from refextract.documents.pdf import convert_PDF_to_plaintext
from refextract.references.config import (
    CFG_REFEXTRACT_MARKER_CLOSING_ARXIV,
    CFG_REFEXTRACT_MARKER_CLOSING_AUTHOR_ETAL,
    CFG_REFEXTRACT_MARKER_CLOSING_AUTHOR_INCL,
    CFG_REFEXTRACT_MARKER_CLOSING_AUTHOR_STND,
    CFG_REFEXTRACT_MARKER_CLOSING_PAGE,
    CFG_REFEXTRACT_MARKER_CLOSING_REPORT_NUM,
    CFG_REFEXTRACT_MARKER_CLOSING_SERIES,
    CFG_REFEXTRACT_MARKER_CLOSING_TITLE,
    CFG_REFEXTRACT_MARKER_CLOSING_TITLE_IBID,
    CFG_REFEXTRACT_MARKER_CLOSING_VOLUME,
    CFG_REFEXTRACT_MARKER_CLOSING_YEAR,
)
from refextract.references.errors import UnknownDocumentTypeError
from refextract.references.kbs import get_kbs
from refextract.references.record import build_references
from refextract.references.regexs import (
    get_reference_line_numeration_marker_patterns,
    re_hdl,
    re_numeration_no_ibid_txt,
    re_recognised_numeration_title_plus_series,
    re_roman_numbers,
    re_tagged_citation,
    re_year_in_misc_txt,
    regex_match_list,
    remove_year,
)
from refextract.references.tag import (
    extract_series_from_volume,
    find_numeration,
    identify_and_tag_DOI,
    identify_and_tag_URLs,
    sum_2_dictionaries,
    tag_reference_line,
)
from refextract.references.text import wash_and_repair_reference_line

LOGGER = logging.getLogger(__name__)

description = """
Refextract tries to extract the reference section from a full-text document.
Extracted reference lines are processed and any recognised citations are
marked up using MARC XML. Recognises author names, URL's, DOI's, and also
journal titles and report numbers as per the relevant knowledge bases. Results
are output to the standard output stream as default, or instead to an xml file.

"""

# General initiation tasks:

# components relating to the standardisation and
# recognition of citations in reference lines:


def remove_reference_line_marker(line):
    """Trim a reference line's 'marker' from the beginning of the line.
       @param line: (string) - the reference line.
       @return: (tuple) containing two strings:
                 + The reference line's marker (or if there was not one,
                   a 'space' character.
                 + The reference line with it's marker removed from the
                   beginning.
    """
    # Get patterns to identify reference-line marker patterns:
    marker_patterns = get_reference_line_numeration_marker_patterns()
    line = line.lstrip()

    marker_match = regex_match_list(line, marker_patterns)

    if marker_match is not None:
        # found a marker:
        marker_val = marker_match.group(u'mark')
        # trim the marker from the start of the line:
        line = line[marker_match.end():].lstrip()
    else:
        marker_val = u" "
    return (marker_val, line)


def roman2arabic(num):
    """Convert numbers from roman to arabic

    This function expects a string like XXII
    and outputs an integer
    """
    t = 0
    p = 0
    for r in num:
        n = 10 ** (205558 % ord(r) % 7) % 9995
        t += n - 2 * p % n
        p = n
    return t


# Transformations

def format_volume(citation_elements):
    """format volume number (roman numbers to arabic)

    When the volume number is expressed in roman numbers (CXXII),
    they are converted to their equivalent in arabic numbers (42)
    """
    re_roman = re.compile(re_roman_numbers + u'$', re.UNICODE)
    for el in citation_elements:
        if el['type'] == 'JOURNAL' and re_roman.match(el['volume']):
            el['volume'] = str(roman2arabic(el['volume'].upper()))
    return citation_elements


def handle_special_journals(citation_elements, kbs):
    """format special journals (like JHEP) volume number

    JHEP needs the volume number prefixed with the year
    e.g. JHEP 0301 instead of JHEP 01
    """
    for el in citation_elements:
        if el['type'] == 'JOURNAL' and el['title'] in kbs['special_journals']:
            if re.match(r'\d{1,2}$', el['volume']):
                # Sometimes the page is omitted and the year is written in its place
                # We can never be sure but it's very likely that page > 1900 is
                # actually a year, so we skip this reference
                if el['year'] == '' and re.match(r'(19|20)\d{2}$', el['page']):
                    el['type'] = 'MISC'
                    el['misc_txt'] = "%s,%s,%s" \
                        % (el['title'], el['volume'], el['page'])
                el['volume'] = el['year'][-2:] + '%02d' % int(el['volume'])
            if el['page'].isdigit():
                # JHEP and JCAP have always pages 3 digits long
                el['page'] = '%03d' % int(el['page'])

    return citation_elements


def format_report_number(citation_elements):
    """Format report numbers that are missing a dash

    e.g. CERN-LCHH2003-01 to CERN-LHCC-2003-01
    """
    re_report = re.compile(r'^(?P<name>[A-Z-]+)(?P<nums>[\d-]+)$', re.UNICODE)
    for el in citation_elements:
        if el['type'] == 'REPORTNUMBER':
            m = re_report.match(el['report_num'])
            if m:
                name = m.group('name')
                if not name.endswith('-'):
                    el['report_num'] = m.group('name') + '-' + m.group('nums')
    return citation_elements


def format_hep(citation_elements):
    """Format hep-th report numbers with a dash

    e.g. replaces hep-th-9711200 with hep-th/9711200
    """
    prefixes = ('astro-ph-', 'hep-th-', 'hep-ph-', 'hep-ex-', 'hep-lat-',
                'math-ph-')
    for el in citation_elements:
        if el['type'] == 'REPORTNUMBER':
            for p in prefixes:
                if el['report_num'].startswith(p):
                    el['report_num'] = el['report_num'][:len(p) - 1] + '/' + \
                        el['report_num'][len(p):]
    return citation_elements


def format_author_ed(citation_elements):
    """Standardise to (ed.) and (eds.)

    e.g. Remove extra space in (ed. )
    """
    for el in citation_elements:
        if el['type'] == 'AUTH':
            el['auth_txt'] = el['auth_txt'].replace('(ed. )', '(ed.)')
            el['auth_txt'] = el['auth_txt'].replace('(eds. )', '(eds.)')
    return citation_elements


def look_for_books(citation_elements, kbs):
    """Look for books in our kb

    Create book tags by using the authors and the title to find books
    in our knowledge base
    """
    title = None
    for el in citation_elements:
        if el['type'] == 'QUOTED':
            title = el
            break

    if title:
        normalized_title = title['title'].upper()
        if normalized_title in kbs['books']:
            line = kbs['books'][normalized_title]
            el = {'type': 'BOOK',
                  'misc_txt': '',
                  'authors': line[0],
                  'title': line[1],
                  'year': line[2].strip(';')}
            citation_elements.append(el)
            citation_elements.remove(title)

    return citation_elements


def split_volume_from_journal(citation_elements):
    """Split volume from journal title

    We need this because sometimes the volume is attached to the journal title
    instead of the volume. In those cases we move it here from the title to the
    volume
    """
    for el in citation_elements:
        if el['type'] == 'JOURNAL' and ';' in el['title']:
            el['title'], series = el['title'].rsplit(';', 1)
            el['volume'] = series + el['volume']
    return citation_elements


def remove_b_for_nucl_phys(citation_elements):
    """Removes b from the volume of some journals

    Removes the B from the volume for Nucl.Phys.Proc.Suppl. because in INSPIRE
    that journal is handled differently.
    """
    for el in citation_elements:
        if el['type'] == 'JOURNAL' and el['title'] == 'Nucl.Phys.Proc.Suppl.' \
                and 'volume' in el \
                and (el['volume'].startswith('b') or el['volume'].startswith('B')):
            el['volume'] = el['volume'][1:]
    return citation_elements


def mangle_volume(citation_elements):
    """Make sure the volume letter is before the volume number

    e.g. transforms 100B to B100
    """
    volume_re = re.compile(r"(\d+)([A-Z])", re.U | re.I)
    for el in citation_elements:
        if el['type'] == 'JOURNAL':
            matches = volume_re.match(el['volume'])
            if matches:
                el['volume'] = matches.group(2) + matches.group(1)

    return citation_elements


def associate_recids(citation_elements, linker_callback):
    for el in citation_elements:
        try:
            el['recid'] = linker_callback(el)
        except (IndexError, KeyError):
            el['recid'] = None
    return citation_elements


def split_needed(next_el, current_types, last_type):
    repeatable_if_adjacent = {"REPORTNUMBER", "COLLABORATION"}
    next_type = "ARXIV" if next_el.get("is_arxiv") else next_el["type"]

    if ";" in next_el["misc_txt"]:
        return "semicolon"
    if (
        next_type in current_types - repeatable_if_adjacent or
        (last_type == next_type and next_type not in repeatable_if_adjacent)
    ):
        return "repeated field"
    return None


def postpone_last_auth(current_citation, num_auth):
    if num_auth == 0:
        return None

    func = current_citation.__getitem__ if num_auth == 1 else current_citation.pop

    for idx, el in enumerate(reversed(current_citation), 1):
        if el["type"] == "AUTH":
            return func(-idx)


def split_citations_iter(citation_elements):
    """Generator splitting a citation line into multiple citations.

    This needs to be done when there are citations to several papers on the
    same line, and uses the simple heuristic that if some non-repeatable fields
    are repeated, then they signal the start of a new citation. Some additional
    care is taken to handle authors correctly.
    """
    current_citation = []
    current_types = set()
    last_type = None
    num_auth = 0
    postponed_auth = None
    prev_split_reason = None

    for el in citation_elements:
        split_reason = split_needed(el, current_types, last_type)
        if split_reason:
            if split_reason == "semicolon":
                misc, el["misc_txt"] = el["misc_txt"].split(";", 1)
                current_citation.append({"type": "MISC", "misc_txt": misc})
            if postponed_auth and (
                num_auth == 0 or
                prev_split_reason == "repeated field"
            ):
                current_citation.insert(0, postponed_auth)
                num_auth += 1
            postponed_auth = postpone_last_auth(current_citation, num_auth)
            yield current_citation

            current_citation = []
            current_types = set()
            last_type = None
            num_auth = 0
            prev_split_reason = split_reason

        current_citation.append(el)

        if el["type"] == "MISC":
            continue
        if el["type"] == "AUTH":
            num_auth += 1
            # detection of authors has many false positives, don't take them
            # into account for splitting
            continue
        last_type = "ARXIV" if el.get("is_arxiv") else el["type"]
        current_types.add(last_type)

    if postponed_auth and (
        num_auth == 0 or
        prev_split_reason == "repeated field"
    ):
        current_citation.insert(0, postponed_auth)
    yield current_citation


def valid_citation(citation):
    els_to_remove = ('MISC', )
    return any(el['type'] not in els_to_remove for el in citation)


def remove_invalid_references(splitted_citations):
    def add_misc(el, txt):
        if not el.get('misc_txt'):
            el['misc_txt'] = txt
        else:
            el['misc_txt'] += " " + txt

    splitted_citations = [citation for citation in splitted_citations
                          if citation]

    # We merge some elements in here which means it only makes sense when
    # we have at least 2 elements to merge together
    if len(splitted_citations) > 1:
        previous_citation = None
        for citation in splitted_citations:
            if not valid_citation(citation):
                # Merge to previous one misc txt
                if previous_citation:
                    citation_to_merge_into = previous_citation
                else:
                    citation_to_merge_into = splitted_citations[1]

                for el in citation:
                    add_misc(citation_to_merge_into[-1], el['misc_txt'])

            previous_citation = citation

    return [citation for citation in splitted_citations
            if valid_citation(citation)]


def merge_invalid_references(splitted_citations):
    def add_misc(el, txt):
        if not el.get('misc_txt'):
            el['misc_txt'] = txt
        else:
            el['misc_txt'] += " " + txt

    splitted_citations = [citation for citation in splitted_citations
                          if citation]

    # We merge some elements in here which means it only makes sense when
    # we have at least 2 elements to merge together
    if len(splitted_citations) > 1:
        previous_citation = None
        previous_citation_valid = True
        for citation in splitted_citations:
            current_citation_valid = valid_citation(citation)
            if not current_citation_valid and not previous_citation_valid:
                # Merge to previous one misc txt
                for el in citation:
                    add_misc(previous_citation[-1], el['misc_txt'])

            previous_citation = citation
            previous_citation_valid = current_citation_valid

    return [citation for citation in splitted_citations
            if valid_citation(citation)]


def add_year_elements(splitted_citations):
    for citation in splitted_citations:
        for el in citation:
            if el['type'] == 'YEAR':
                continue

        year = None
        for el in citation:
            if el['type'] == 'JOURNAL' or el['type'] == 'BOOK' \
                    and 'year' in el:
                year = el['year']
                break

        if not year:
            for el in citation:
                m = re_year_in_misc_txt.search(el['misc_txt'])
                if m:
                    year = m.group(0)

        if year:
            citation.append({'type': 'YEAR',
                             'year': year,
                             'misc_txt': '',
                             })
            for el in citation:
                if year in el['misc_txt']:
                    el['misc_txt'] = remove_year(el['misc_txt'], year)

    return splitted_citations


def look_for_implied_ibids(splitted_citations):
    def look_for_journal(els):
        return any(el['type'] == 'JOURNAL' for el in els)

    current_journal = None
    for citation in splitted_citations:
        if current_journal and not look_for_journal(citation):
            for el in citation:
                if el['type'] == 'MISC':
                    numeration = find_numeration(el['misc_txt'])
                    if numeration:
                        if not numeration['series']:
                            numeration['series'] = extract_series_from_volume(
                                current_journal['volume'])
                        if numeration['series']:
                            volume = numeration[
                                'series'] + numeration['volume']
                        else:
                            volume = numeration['volume']
                        ibid_el = {'type': 'JOURNAL',
                                   'misc_txt': '',
                                   'title': current_journal['title'],
                                   'volume': volume,
                                   'year': numeration['year'],
                                   'page': numeration['page'] or
                                           numeration['jinst_page'],
                                   'page_end': numeration['page_end'],
                                   'is_ibid': True,
                                   'extra_ibids': []}
                        citation.append(ibid_el)
                        el['misc_txt'] = el['misc_txt'][numeration['len']:]

        current_journal = None
        for el in citation:
            if el['type'] == 'JOURNAL':
                current_journal = el

    return splitted_citations


def remove_duplicated_authors(splitted_citations):
    for citation in splitted_citations:
        found_author = False
        for el in citation:
            if el['type'] == 'AUTH':
                if found_author:
                    el['type'] = 'MISC'
                    el['misc_txt'] = el['misc_txt'] + " " + el['auth_txt']
                else:
                    found_author = True

    return splitted_citations


def remove_duplicated_dois(splitted_citations):
    for citation in splitted_citations:
        found_doi = False
        for el in citation[:]:
            if el['type'] == 'DOI':
                if found_doi:
                    citation.remove(el)
                else:
                    found_doi = True

    return splitted_citations


def remove_duplicated_collaborations(splitted_citations):
    for citation in splitted_citations:
        collabs = []
        for el in citation[:]:
            if el['type'] == 'COLLABORATION':
                if el['collaboration'] in collabs:
                    citation.remove(el)
                else:
                    collabs.append(el['collaboration'])

    return splitted_citations


def add_recid_elements(splitted_citations):
    for citation in splitted_citations:
        for el in citation:
            if el.get('recid', None):
                citation.append({'type': 'RECID',
                                 'recid': el['recid'],
                                 'misc_txt': ''})
                break


def arxiv_urls_to_report_numbers(citation_elements):
    arxiv_url_prefix = 'http://arxiv.org/abs/'
    for el in citation_elements:
        if el['type'] == 'URL' and el['url_string'].startswith(arxiv_url_prefix):
            el['type'] = 'REPORTNUMBER'
            el['report_num'] = el['url_string'].replace(arxiv_url_prefix, 'arXiv:')


def look_for_hdl(citation_elements):
    """Looks for handle identifiers in the misc txt of the citation elements

       When finding an hdl, creates a new HDL element.
       @param citation_elements: (list) elements to process
    """
    for el in list(citation_elements):
        matched_hdl = re_hdl.finditer(el['misc_txt'])
        for match in reversed(list(matched_hdl)):
            hdl_el = {'type': 'HDL',
                      'hdl_id': match.group('hdl_id'),
                      'misc_txt': el['misc_txt'][match.end():]}
            el['misc_txt'] = el['misc_txt'][0:match.start()]
            citation_elements.insert(citation_elements.index(el) + 1, hdl_el)


def look_for_hdl_urls(citation_elements):
    """Looks for handle identifiers that have already been identified as urls

       When finding an hdl, creates a new HDL element.
       @param citation_elements: (list) elements to process
    """
    for el in citation_elements:
        if el['type'] == 'URL':
            match = re_hdl.match(el['url_string'])
            if match:
                el['type'] = 'HDL'
                el['hdl_id'] = match.group('hdl_id')
                del el['url_desc']
                del el['url_string']


# End of elements transformations

def print_citations(splitted_citations, line_marker):
    LOGGER.debug(u'split_citations')
    LOGGER.debug(u"line marker %s", line_marker)
    for citation in splitted_citations:
        LOGGER.debug(u"elements")
        for el in citation:
            LOGGER.debug('%s %s', el['type'], repr(el))


def parse_reference_line(ref_line, kbs, bad_titles_count=None, linker_callback=None):
    """Parse one reference line

    @input a string representing a single reference bullet
    @output parsed references (a list of elements objects)
    """
    # Strip the 'marker' (e.g. [1]) from this reference line:
    if bad_titles_count is None:
        bad_titles_count = {}
    line_marker, ref_line = remove_reference_line_marker(ref_line)
    # Find DOI sections in citation
    ref_line, identified_dois = identify_and_tag_DOI(ref_line)
    # Identify and replace URLs in the line:
    ref_line, identified_urls = identify_and_tag_URLs(ref_line)
    # Tag <cds.JOURNAL>, etc.
    tagged_line, bad_titles_count = tag_reference_line(ref_line,
                                                       kbs,
                                                       bad_titles_count)

    # Debug print tagging (authors, titles, volumes, etc.)
    LOGGER.debug("tags %r", tagged_line)

    # Using the recorded information, create a MARC XML representation
    # of the rebuilt line:
    # At the same time, get stats of citations found in the reference line
    # (titles, urls, etc):
    citation_elements, line_marker, counts = \
        parse_tagged_reference_line(line_marker,
                                    tagged_line,
                                    identified_dois,
                                    identified_urls)

    # Transformations on elements
    split_volume_from_journal(citation_elements)
    format_volume(citation_elements)
    handle_special_journals(citation_elements, kbs)
    format_report_number(citation_elements)
    format_author_ed(citation_elements)
    look_for_books(citation_elements, kbs)
    format_hep(citation_elements)
    remove_b_for_nucl_phys(citation_elements)
    mangle_volume(citation_elements)
    arxiv_urls_to_report_numbers(citation_elements)
    look_for_hdl(citation_elements)
    look_for_hdl_urls(citation_elements)

    # Link references if desired
    if linker_callback:
        associate_recids(citation_elements, linker_callback)

    # Split the reference in multiple ones if needed
    splitted_citations = list(split_citations_iter(citation_elements))

    # Look for implied ibids
    look_for_implied_ibids(splitted_citations)
    # Find year
    add_year_elements(splitted_citations)
    # Look for books in misc field
    look_for_undetected_books(splitted_citations, kbs)

    if linker_callback:
        # Link references with the newly added ibids/books information
        for citations in splitted_citations:
            associate_recids(citations, linker_callback)

    # FIXME: Needed?
    # Remove references with only misc text
    # splitted_citations = remove_invalid_references(splitted_citations)
    # Merge references with only misc text
    # splitted_citations = merge_invalid_references(splitted_citations)

    remove_duplicated_authors(splitted_citations)
    remove_duplicated_dois(splitted_citations)
    remove_duplicated_collaborations(splitted_citations)
    add_recid_elements(splitted_citations)

    # For debugging purposes
    print_citations(splitted_citations, line_marker)

    return splitted_citations, line_marker, counts, bad_titles_count


def year_from_citation(citation):
    citation_year = None

    for el in citation:
        if el['type'] == 'YEAR':
            citation_year = el['year']
            break

    return citation_year


def look_for_undetected_books(splitted_citations, kbs):
    for citation in splitted_citations:
        if is_unknown_citation(citation):
            search_for_book_in_misc(citation, kbs)


def search_for_book_in_misc(citation, kbs):
    """Searches for books in the misc_txt field
    if the citation is not recognized as anything like a journal, book, etc.
    """
    citation_year = year_from_citation(citation)
    for citation_element in citation:
        LOGGER.debug(u"Searching for book title in: %s", citation_element['misc_txt'])
        for title in kbs['books']:
            startIndex = find_substring_ignore_special_chars(
                citation_element['misc_txt'], title)
            if startIndex != -1:
                line = kbs['books'][title.upper()]
                book_year = line[2].strip(';')
                book_authors = line[0]
                book_found = False
                if citation_year == book_year:
                    # For now consider the citation as valid, we are using
                    # an exact search, we don't need to check the authors
                    # However, the code below will be useful if we decide
                    # to introduce fuzzy matching.
                    book_found = True

                    for author in get_possible_author_names(citation):
                        if find_substring_ignore_special_chars(
                                book_authors, author) != -1:
                            book_found = True

                    for author in re.findall('[a-zA-Z]{4,}', book_authors):
                        if find_substring_ignore_special_chars(
                                citation_element['misc_txt'],
                                author) != -1:
                            book_found = True

                    if book_found:
                        LOGGER.debug(u"Book found: %s", title)
                        book_element = {'type': 'BOOK',
                                        'misc_txt': '',
                                        'authors': book_authors,
                                        'title': line[1],
                                        'year': book_year}
                        citation.append(book_element)
                        citation_element['misc_txt'] = cut_substring_with_special_chars(
                            citation_element['misc_txt'], title, startIndex)
                        # Remove year from misc txt
                        citation_element['misc_txt'] = remove_year(
                            citation_element['misc_txt'], book_year)
                        return True

        LOGGER.debug("Book not found!")

    return False


def get_possible_author_names(citation):
    for citation_element in citation:
        if citation_element['type'] == 'AUTH':
            return re.findall('[a-zA-Z]{4,}', citation_element['auth_txt'])
    return []


def find_substring_ignore_special_chars(s, substr):
    s = s.upper()
    substr = substr.upper()
    clean_s, dummy_subs_in_s = re.subn('[^A-Z0-9]', '', s)
    clean_substr, dummy_subs_in_substr = re.subn('[^A-Z0-9]', '', substr)
    startIndex = clean_s.find(clean_substr)
    if startIndex != -1:
        i = 0
        real_index = 0
        re_alphanum = re.compile('[A-Z0-9]')
        for char in s:
            if re_alphanum.match(char):
                i += 1
            if i > startIndex:
                break
            real_index += 1

        return real_index
    else:
        return -1


def cut_substring_with_special_chars(s, sub, startIndex):
    counter = 0
    subPosition = 0
    s_Upper = s.upper()
    sub = sub.upper()
    clean_sub = re.sub('[^A-Z0-9]', '', sub)
    for char in s_Upper[startIndex:]:
        if char == clean_sub[subPosition]:
            subPosition += 1
        counter += 1
        # end of substrin reached?
        if subPosition >= len(clean_sub):
            # include everything till a space, open bracket or a normal
            # character
            counter += len(re.split('[ [{(a-zA-Z0-9]', s[startIndex + counter:],
                                    maxsplit=1)[0])

            return s[0:startIndex].strip() + ' ' + s[startIndex + counter:].strip()


def is_unknown_citation(citation):
    """Checks if the citation got recognized as one of the known types.
    """
    knownTypes = ['BOOK', 'JOURNAL', 'DOI', 'ISBN', 'RECID']
    return all(
        citation_element['type'] not in knownTypes for citation_element in citation)


def parse_references_elements(ref_sect, kbs, linker_callback=None):
    """Passed a complete reference section, process each line and attempt to
       ## identify and standardise individual citations within the line.
       @param ref_sect: (list) of strings - each string in the list is a
        reference line.
       @param preprint_repnum_search_kb: (dictionary) - keyed by a tuple
        containing the line-number of the pattern in the KB and the non-standard
        category string.  E.g.: (3, 'ASTRO PH'). Value is regexp pattern used to
        search for that report-number.
       @param preprint_repnum_standardised_categs: (dictionary) - keyed by non-
        standard version of institutional report number, value is the
        standardised version of that report number.
       @param periodical_title_search_kb: (dictionary) - keyed by non-standard
        title to search for, value is the compiled regexp pattern used to
        search for that title.
       @param standardised_periodical_titles: (dictionary) - keyed by non-
        standard title to search for, value is the standardised version of that
        title.
       @param periodical_title_search_keys: (list) - ordered list of non-
        standard titles to search for.
       @return: (tuple) of 6 components:
         ( list       -> of strings, each string is a MARC XML-ized reference
                         line.
           integer    -> number of fields of miscellaneous text found for the
                         record.
           integer    -> number of title citations found for the record.
           integer    -> number of institutional report-number citations found
                         for the record.
           integer    -> number of URL citations found for the record.
           integer    -> number of DOI's found
           integer    -> number of author groups found
           dictionary -> The totals for each 'bad title' found in the reference
                         section.
         )
    """
    # a list to contain the processed reference lines:
    citations = []
    # counters for extraction stats:
    counts = {
        'misc': 0,
        'title': 0,
        'reportnum': 0,
        'url': 0,
        'doi': 0,
        'auth_group': 0,
    }
    # A dictionary to contain the total count of each 'bad title' found
    # in the entire reference section:
    bad_titles_count = {}

    # Cleanup the reference lines

    # process references line-by-line:
    for ref_line in ref_sect:
        clean_line = wash_and_repair_reference_line(ref_line)

        citation_elements, line_marker, this_counts, bad_titles_count = \
            parse_reference_line(
                clean_line, kbs, bad_titles_count, linker_callback)

        # Accumulate stats
        counts = sum_2_dictionaries(counts, this_counts)

        citations.append({'elements': citation_elements,
                          'line_marker': line_marker,
                          'raw_ref': ref_line})

    # Return the list of processed reference lines:
    return citations, counts, bad_titles_count


def parse_tagged_reference_line(line_marker,
                                line,
                                identified_dois,
                                identified_urls):
    """ Given a single tagged reference line, convert it to its MARC-XML representation.
    Try to find all tags and extract their contents and their types into corresponding
    dictionary elements. Append each dictionary tag representation onto a list, which
    is given to 'build_formatted_xml_citation()'
    where the correct xml output will be generated.

    This method is dumb, with very few heuristics.
    It simply looks for tags, and makes dictionaries
    from the data it finds in a tagged reference line.

    @param line_marker: (string) The line marker for
    this single reference line (e.g. [19])
    @param line: (string) The tagged reference line.
    @param identified_dois: (list) a list of dois which were found in this line.
    The ordering of dois corresponds to the ordering of tags in the line,
     reading from left to right.
    @param identified_urls: (list) a list of urls which were found in this line.
    The ordering of urls corresponds to the ordering of tags in the line,
    reading from left to right.
    @param which format to use for references,
    roughly "<title> <volume> <page>" or "<title>,<volume>,<page>"
    @return xml_line: (string) the MARC-XML representation of the tagged reference line
    @return count_*: (integer) the number of * (pieces of info)
    found in the reference line.
    """
    count_misc = 0
    count_title = 0
    count_reportnum = 0
    count_url = 0
    count_doi = 0
    count_auth_group = 0
    processed_line = line
    cur_misc_txt = u""

    tag_match = re_tagged_citation.search(processed_line)

    # contains a list of dictionary entries of previously cited items
    citation_elements = []
    # the last tag element found when working from left-to-right across the
    # line
    identified_citation_element = None

    while tag_match is not None:
        # While there are tags inside this reference line...
        tag_match_start = tag_match.start()
        tag_match_end = tag_match.end()
        tag_type = tag_match.group(1)
        cur_misc_txt += processed_line[0:tag_match_start]

        # Catches both standard titles, and ibid's
        if tag_type.find("JOURNAL") != -1:
            # This tag is an identified journal TITLE. It should be followed
            # by VOLUME, YEAR and PAGE tags.

            # See if the found title has been tagged as an ibid:
            # <cds.JOURNALibid>
            if tag_match.group('ibid'):
                is_ibid = True
                closing_tag_length = len(
                    CFG_REFEXTRACT_MARKER_CLOSING_TITLE_IBID)
                idx_closing_tag = processed_line.find(
                    CFG_REFEXTRACT_MARKER_CLOSING_TITLE_IBID,
                    tag_match_end)
            else:
                is_ibid = False
                closing_tag_length = len(CFG_REFEXTRACT_MARKER_CLOSING_TITLE)
                # extract the title from the line:
                idx_closing_tag = processed_line.find(
                    CFG_REFEXTRACT_MARKER_CLOSING_TITLE,
                    tag_match_end)

            if idx_closing_tag == -1:
                # no closing TITLE tag found - get rid of the solitary tag
                processed_line = processed_line[tag_match_end:]
                identified_citation_element = None
            else:

                # Closing tag was found:
                # The title text to be used in the marked-up citation:
                title_text = processed_line[tag_match_end:idx_closing_tag]

                # Now trim this matched title and its tags from the start of
                # the line:
                processed_line = processed_line[
                    idx_closing_tag + closing_tag_length:]

                numeration_match = re_recognised_numeration_title_plus_series.search(
                    processed_line)
                if numeration_match:
                    # recognised numeration immediately after the title -
                    # extract it:
                    reference_volume = numeration_match.group('vol')
                    reference_year = numeration_match.group('yr') or ''
                    reference_page = numeration_match.group('pg')

                    # This is used on two accounts:
                    # 1. To get the series char from the title,
                    #   if no series was found with the numeration
                    # 2. To always remove any series character from the title match text
                    # series_from_title = re_series_from_title.search(title_text)
                    #
                    if numeration_match.group('series'):
                        reference_volume = numeration_match.group(
                            'series') + reference_volume

                    # Skip past the matched numeration in the working line:
                    processed_line = processed_line[numeration_match.end():]

                    # 'id_ibid' saves whether THIS TITLE is an ibid or not. (Boolean)
                    # 'extra_ibids' are there to hold ibid's without the word 'ibid',
                    # which come directly after this title
                    # i.e., they are recognised using title numeration instead
                    # of ibid notation
                    identified_citation_element = {'type': "JOURNAL",
                                                   'misc_txt': cur_misc_txt,
                                                   'title': title_text,
                                                   'volume': reference_volume,
                                                   'year': reference_year,
                                                   'page': reference_page,
                                                   'is_ibid': is_ibid,
                                                   'extra_ibids': []
                                                   }
                    count_title += 1
                    cur_misc_txt = u""

                    # Try to find IBID's after this title,
                    # on top of previously found titles that were
                    # denoted with the word 'IBID'.
                    # (i.e. look for IBID's without the word 'IBID' by
                    # looking at extra numeration after this title)

                    numeration_match = re_numeration_no_ibid_txt.match(
                        processed_line)
                    while numeration_match is not None:

                        reference_volume = numeration_match.group('vol')
                        reference_year = numeration_match.group('yr')
                        reference_page = numeration_match.group('pg')

                        if numeration_match.group('series'):
                            reference_volume = numeration_match.group(
                                'series') + reference_volume

                        # Skip past the matched numeration in the working line:
                        processed_line = processed_line[
                            numeration_match.end():]

                        # Takes the just found title text
                        identified_citation_element['extra_ibids'].append(
                            {'type': "JOURNAL",
                             'misc_txt': "",
                             'title': title_text,
                             'volume': reference_volume,
                             'year': reference_year,
                             'page': reference_page,
                             })
                        # Increment the stats counters:
                        count_title += 1

                        title_text = ""
                        reference_volume = ""
                        reference_year = ""
                        reference_page = ""
                        numeration_match = re_numeration_no_ibid_txt.match(
                            processed_line)
                else:
                    # No numeration was recognised after the title. Add the
                    # title into a MISC item instead:
                    cur_misc_txt += "%s" % title_text
                    identified_citation_element = None

        elif tag_type == "REPORTNUMBER":

            # This tag is an identified institutional report number:

            # extract the institutional report-number from the line:
            idx_closing_tag = processed_line.find(
                CFG_REFEXTRACT_MARKER_CLOSING_REPORT_NUM, tag_match_end)
            # Sanity check - did we find a closing report-number tag?
            if idx_closing_tag == -1:
                # no closing </cds.REPORTNUMBER> tag found -
                # strip the opening tag and move past this
                # recognised reportnumber as it is unreliable:
                processed_line = processed_line[tag_match_end:]
                identified_citation_element = None
            else:
                # closing tag was found
                report_num = processed_line[tag_match_end:idx_closing_tag]
                # now trim this matched institutional report-number
                # and its tags from the start of the line:
                ending_tag_pos = idx_closing_tag \
                    + len(CFG_REFEXTRACT_MARKER_CLOSING_REPORT_NUM)
                processed_line = processed_line[ending_tag_pos:]

                identified_citation_element = {'type': "REPORTNUMBER",
                                               'misc_txt': cur_misc_txt,
                                               'report_num': report_num}
                count_reportnum += 1
                cur_misc_txt = u""

        elif tag_type == "ARXIV":

            # This tag is an arXiv eprint:

            # extract the institutional report-number from the line:
            idx_closing_tag = processed_line.find(CFG_REFEXTRACT_MARKER_CLOSING_ARXIV,
                                                  tag_match_end)
            # Sanity check - did we find a closing report-number tag?
            if idx_closing_tag == -1:
                # no closing </cds.ARXIV> tag found -
                # strip the opening tag and move past this
                # recognised arXiv as it is unreliable:
                processed_line = processed_line[tag_match_end:]
                identified_citation_element = None
            else:
                # closing tag was found
                report_num = processed_line[tag_match_end:idx_closing_tag]
                # now trim this matched institutional report-number
                # and its tags from the start of the line:
                ending_tag_pos = idx_closing_tag \
                    + len(CFG_REFEXTRACT_MARKER_CLOSING_ARXIV)
                processed_line = processed_line[ending_tag_pos:]

                identified_citation_element = {'type': "REPORTNUMBER",
                                               'misc_txt': cur_misc_txt,
                                               'report_num': report_num,
                                               'is_arxiv': True}
                count_reportnum += 1
                cur_misc_txt = u""

        elif tag_type == "URL":
            # This tag is an identified URL:

            # From the "identified_urls" list, get this URL and its
            # description string:
            url_string = identified_urls[0][0]
            url_desc = identified_urls[0][1]

            # Now move past this "<cds.URL />"tag in the line:
            processed_line = processed_line[tag_match_end:]

            # Delete the information for this URL from the start of the list
            # of identified URLs:
            identified_urls[0:1] = []

            # Save the current misc text
            identified_citation_element = {
                'type': "URL",
                'misc_txt': "%s" % cur_misc_txt,
                'url_string': "%s" % url_string,
                'url_desc': "%s" % url_desc
            }

            count_url += 1
            cur_misc_txt = u""

        elif tag_type == "DOI":
            # This tag is an identified DOI:

            # From the "identified_dois" list, get this DOI and its
            # description string:
            doi_string = identified_dois[0]

            # Now move past this "<cds.CDS />"tag in the line:
            processed_line = processed_line[tag_match_end:]

            # Remove DOI from the list of DOI strings
            identified_dois[0:1] = []

            # SAVE the current misc text
            identified_citation_element = {
                'type': "DOI",
                'misc_txt': "%s" % cur_misc_txt,
                'doi_string': "%s" % doi_string
            }

            # Increment the stats counters:
            count_doi += 1
            cur_misc_txt = u""

        elif tag_type.find("AUTH") != -1:
            # This tag is an identified Author:

            auth_type = ""
            # extract the title from the line:
            if tag_type.find("stnd") != -1:
                auth_type = "stnd"
                idx_closing_tag_nearest = processed_line.find(
                    CFG_REFEXTRACT_MARKER_CLOSING_AUTHOR_STND, tag_match_end)
            elif tag_type.find("etal") != -1:
                auth_type = "etal"
                idx_closing_tag_nearest = processed_line.find(
                    CFG_REFEXTRACT_MARKER_CLOSING_AUTHOR_ETAL, tag_match_end)
            elif tag_type.find("incl") != -1:
                auth_type = "incl"
                idx_closing_tag_nearest = processed_line.find(
                    CFG_REFEXTRACT_MARKER_CLOSING_AUTHOR_INCL, tag_match_end)

            if idx_closing_tag_nearest == -1:
                # no closing </cds.AUTH****> tag found - strip the opening tag
                # and move past it
                processed_line = processed_line[tag_match_end:]
                identified_citation_element = None
            else:
                auth_txt = processed_line[
                    tag_match_end:idx_closing_tag_nearest]
                # Now move past the ending tag in the line:
                processed_line = processed_line[
                    idx_closing_tag_nearest + len("</cds.AUTHxxxx>"):]
                # SAVE the current misc text
                identified_citation_element = {
                    'type': "AUTH",
                    'misc_txt': "%s" % cur_misc_txt,
                    'auth_txt': "%s" % auth_txt,
                    'auth_type': "%s" % auth_type
                }

                # Increment the stats counters:
                count_auth_group += 1
                cur_misc_txt = u""

        # These following tags may be found separately;
        # They are usually found when a "JOURNAL" tag is hit
        # (ONLY immediately afterwards, however)
        # Sitting by themselves means they do not have
        # an associated TITLE tag, and should be MISC
        elif tag_type == "SER":
            # This tag is a SERIES tag; Since it was not preceeded by a TITLE
            # tag, it is useless - strip the tag and put it into miscellaneous:
            (cur_misc_txt, processed_line) = \
                convert_unusable_tag_to_misc(processed_line, cur_misc_txt,
                                             tag_match_end,
                                             CFG_REFEXTRACT_MARKER_CLOSING_SERIES)
            identified_citation_element = None

        elif tag_type == "VOL":
            # This tag is a VOLUME tag; Since it was not preceeded by a TITLE
            # tag, it is useless - strip the tag and put it into miscellaneous:
            (cur_misc_txt, processed_line) = \
                convert_unusable_tag_to_misc(processed_line, cur_misc_txt,
                                             tag_match_end,
                                             CFG_REFEXTRACT_MARKER_CLOSING_VOLUME)
            identified_citation_element = None

        elif tag_type == "YR":
            # This tag is a YEAR tag; Since it's not preceeded by TITLE and
            # VOLUME tags, it is useless - strip the tag and put the contents
            # into miscellaneous:
            (cur_misc_txt, processed_line) = \
                convert_unusable_tag_to_misc(processed_line, cur_misc_txt,
                                             tag_match_end,
                                             CFG_REFEXTRACT_MARKER_CLOSING_YEAR)
            identified_citation_element = None

        elif tag_type == "PG":
            # This tag is a PAGE tag; Since it's not preceeded by TITLE,
            # VOLUME and YEAR tags, it is useless - strip the tag and put the
            # contents into miscellaneous:
            (cur_misc_txt, processed_line) = \
                convert_unusable_tag_to_misc(processed_line, cur_misc_txt,
                                             tag_match_end,
                                             CFG_REFEXTRACT_MARKER_CLOSING_PAGE)
            identified_citation_element = None

        elif tag_type == "QUOTED":
            identified_citation_element, processed_line, cur_misc_txt = \
                map_tag_to_subfield(tag_type,
                                    processed_line[tag_match_end:],
                                    cur_misc_txt,
                                    'title')

        elif tag_type == "ISBN":
            identified_citation_element, processed_line, cur_misc_txt = \
                map_tag_to_subfield(tag_type,
                                    processed_line[tag_match_end:],
                                    cur_misc_txt,
                                    tag_type)

        elif tag_type == "PUBLISHER":
            identified_citation_element, processed_line, cur_misc_txt = \
                map_tag_to_subfield(tag_type,
                                    processed_line[tag_match_end:],
                                    cur_misc_txt,
                                    'publisher')

        elif tag_type == "COLLABORATION":
            identified_citation_element, processed_line, cur_misc_txt = \
                map_tag_to_subfield(tag_type,
                                    processed_line[tag_match_end:],
                                    cur_misc_txt,
                                    'collaboration')

        if identified_citation_element:
            # Append the found tagged data and current misc text
            citation_elements.append(identified_citation_element)
            identified_citation_element = None

        # Look for the next tag in the processed line:
        tag_match = re_tagged_citation.search(processed_line)

    # place any remaining miscellaneous text into the
    # appropriate MARC XML fields:
    cur_misc_txt += processed_line

    # This MISC element will hold the entire citation in the event
    # that no tags were found.
    if len(cur_misc_txt.strip(" .;,")) > 0:
        # Increment the stats counters:
        count_misc += 1
        identified_citation_element = {
            'type': "MISC",
            'misc_txt': cur_misc_txt,
        }
        citation_elements.append(identified_citation_element)

    return (citation_elements, line_marker, {
        'misc': count_misc,
        'title': count_title,
        'reportnum': count_reportnum,
        'url': count_url,
        'doi': count_doi,
        'auth_group': count_auth_group
    })


def map_tag_to_subfield(tag_type, line, cur_misc_txt, dest):
    """Create a new reference element"""
    closing_tag = '</cds.%s>' % tag_type
    # extract the institutional report-number from the line:
    idx_closing_tag = line.find(closing_tag)
    # Sanity check - did we find a closing tag?
    if idx_closing_tag == -1:
        # no closing </cds.TAG> tag found - strip the opening tag and move past this
        # recognised reportnumber as it is unreliable:
        identified_citation_element = None
        line = line[len('<cds.%s>' % tag_type):]
    else:
        tag_content = line[:idx_closing_tag]
        identified_citation_element = {'type': tag_type,
                                       'misc_txt': cur_misc_txt,
                                       dest: tag_content}
        ending_tag_pos = idx_closing_tag + len(closing_tag)
        line = line[ending_tag_pos:]
        cur_misc_txt = u""

    return identified_citation_element, line, cur_misc_txt


def convert_unusable_tag_to_misc(line,
                                 misc_text,
                                 tag_match_end,
                                 closing_tag):
    """Function to remove an unwanted, tagged, citation item from a reference
       line. The tagged item itself is put into the miscellaneous text variable;
       the data up to the closing tag is then trimmed from the beginning of the
       working line. For example, the following working line:
         Example, AN. Testing software; <cds.YR>(2001)</cds.YR>, CERN, Geneva.
       ...would be trimmed down to:
         , CERN, Geneva.
       ...And the Miscellaneous text taken from the start of the line would be:
         Example, AN. Testing software; (2001)
       ...(assuming that the details of <cds.YR> and </cds.YR> were passed to
       the function).
       @param line: (string) - the reference line.
       @param misc_text: (string) - the variable containing the miscellaneous
        text recorded so far.
       @param tag_match_end: (integer) - the index of the end of the opening tag
        in the line.
       @param closing_tag: (string) - the closing tag to look for in the line
        (e.g. </cds.YR>).
       @return: (tuple) - containing misc_text (string) and line (string)
    """

    # extract the tagged information:
    idx_closing_tag = line.find(closing_tag, tag_match_end)
    # Sanity check - did we find a closing tag?
    if idx_closing_tag == -1:
        # no closing tag found - strip the opening tag and move past this
        # recognised item as it is unusable:
        line = line[tag_match_end:]
    else:
        # closing tag was found
        misc_text += line[tag_match_end:idx_closing_tag]
        # now trim the matched item and its tags from the start of the line:
        line = line[idx_closing_tag + len(closing_tag):]
    return (misc_text, line)

# Tasks related to extraction of reference section from full-text:

# ----> 1. Removing page-breaks, headers and footers before
#          searching for reference section:

# ----> 2. Finding reference section in full-text:

# ----> 3. Found reference section - now take out lines and rebuild them:


def remove_leading_garbage_lines_from_reference_section(ref_sectn):
    """Sometimes, the first lines of the extracted references are completely
       blank or email addresses. These must be removed as they are not
       references.
       @param ref_sectn: (list) of strings - the reference section lines
       @return: (list) of strings - the reference section without leading
        blank lines or email addresses.
    """
    p_email = re.compile(r'^\s*e\-?mail', re.UNICODE)
    while ref_sectn and (ref_sectn[0].isspace() or p_email.match(ref_sectn[0])):
        ref_sectn.pop(0)
    return ref_sectn


# ----> Glue - logic for finding and extracting reference section:


# Tasks related to conversion of full-text to plain-text:

def clean_pdf_file(filename):
    """
    strip leading and/or trailing junk from a PDF file
    """
    with open(filename, 'r+b') as file, mmap.mmap(file.fileno(),
                                                  0,
                                                  access=mmap.ACCESS_WRITE) as mmfile:
        start = mmfile.find(b'%PDF-')
        if start == -1:
            # no PDF marker found
            LOGGER.debug('not a PDF file')
            return
        end = mmfile.rfind(b'%%EOF')
        offset = len(b'%%EOF')
        if start > 0:
            LOGGER.debug('moving and truncating')
            mmfile.move(0, start, end + offset - start)
            mmfile.resize(end + offset - start)
            mmfile.flush()
        elif end > 0 and end + offset != mmfile.size():
            LOGGER.debug('truncating only')
            mmfile.resize(end + offset - start)
            mmfile.flush()


def get_plaintext_document_body(fpath, keep_layout=False):
    """Given a file-path to a full-text, return a list of unicode strings
       whereby each string is a line of the fulltext.
       In the case of a plain-text document, this simply means reading the
       contents in from the file. In the case of a PDF however,
       this means converting the document to plaintext.
       It raises UnknownDocumentTypeError if the document is not a PDF or
       plain text.
       @param fpath: (string) - the path to the fulltext file
       @return: (list) of strings - each string being a line in the document.
    """
    textbody = []
    clean_pdf_file(fpath)
    mime_type = magic.from_file(fpath, mime=True)

    if mime_type == "text/plain":
        with open(fpath, "r") as f:
            textbody = f.readlines()
    elif mime_type == "application/pdf":
        textbody = convert_PDF_to_plaintext(fpath, keep_layout)
    else:
        raise UnknownDocumentTypeError(mime_type)

    return textbody


def parse_references(reference_lines,
                     recid=None,
                     override_kbs_files=None,
                     reference_format=u"{title} {volume} ({year}) {page}",
                     linker_callback=None):
    """Parse a list of references

    Given a list of raw reference lines (list of strings),
    output a list of dictionaries containing the parsed references
    """
    # RefExtract knowledge bases
    kbs = get_kbs(custom_kbs=override_kbs_files)
    # Identify journal titles, report numbers, URLs, DOIs, and authors...
    processed_references, counts, dummy_bad_titles_count = \
        parse_references_elements(reference_lines, kbs, linker_callback)

    return (build_references(processed_references, reference_format),
            build_stats(counts))


def build_stats(counts):
    """Return stats information from counts structure."""
    stats = {
        'status': 0,
        'reportnum': counts['reportnum'],
        'title': counts['title'],
        'author': counts['auth_group'],
        'url': counts['url'],
        'doi': counts['doi'],
        'misc': counts['misc'],
    }
    stats_str = ("%(status)s-%(reportnum)s-%(title)s-"
                 "%(author)s-%(url)s-%(doi)s-%(misc)s") % stats
    stats["old_stats_str"] = stats_str
    stats["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return stats
