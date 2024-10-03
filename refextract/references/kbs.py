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

import codecs
import contextlib
import csv
import re

import six

from refextract.documents.text import re_group_captured_multiple_space
from refextract.references.config import CFG_REFEXTRACT_KBS
from refextract.references.regexs import (
    re_extract_char_class,
    re_extract_quoted_text,
    re_kb_line,
    re_punctuation,
    re_regexp_character_class,
)


@contextlib.contextmanager
def file_resolving(fpath, reader=None, **kwargs):
    if isinstance(fpath, six.string_types):
        fh = codecs.open(fpath, encoding='utf-8')
        if reader:
            yield reader(fh,
                         delimiter=kwargs.pop('delimiter', '|'),
                         lineterminator=kwargs.pop('lineterminator', ';'))
        else:
            yield fh

        fh.close()
    else:
        fh = fpath
        yield fh


def get_kbs(custom_kbs=None, cache={}, cache_inputs={}):  # noqa
    """Load kbs (with caching).

    This function stores the loaded kbs into the cache variable.
    For the caching to work, it needs to receive empty dictionaries
    as "cache" and "cache_inputs" parameters.
    """
    kbs = CFG_REFEXTRACT_KBS.copy()
    if custom_kbs:
        kbs.update({kb_type: kb for (kb_type, kb) in custom_kbs.items() if kb})

    for kb_type, kb in kbs.items():
        if kb != cache_inputs.get(kb_type):
            cache_inputs[kb_type] = kb
            cache[kb_type] = load_kb_by_type(kb_type, kb)
    return cache


def load_kb_by_type(kb_type, kb):
    """Load kb (without caching) for a given kb type."""

    loaders = {
        'journals_re': build_journals_re_kb,
        'journals': lambda kb: load_kb(kb, build_journals_kb),
        'report-numbers': build_reportnum_kb,
        'authors': build_authors_kb,
        'books': build_books_kb,
        'publishers': lambda kb: load_kb(kb, build_publishers_kb),
        'special_journals': build_special_journals_kb,
        'collaborations': lambda kb: load_kb(kb, build_collaborations_kb),
    }

    return loaders[kb_type](kb)


def load_kb(path, builder):
    if isinstance(path, dict):
        return load_kb_from_iterable(path.items(), builder)
    elif hasattr(path, 'startswith'):
        return load_kb_from_file(path, builder)
    return load_kb_from_iterable(path, builder)


def order_reportnum_patterns_bylen(numeration_patterns):
    """Given a list of user-defined patterns for recognising the numeration
       styles of an institute's preprint references, for each pattern,
       strip out character classes and record the length of the pattern.
       Then add the length and the original pattern (in a tuple) into a new
       list for these patterns and return this list.
       @param numeration_patterns: (list) of strings, whereby each string is
        a numeration pattern.
       @return: (list) of tuples, where each tuple contains a pattern and
        its length.
    """
    pattern_list = []
    for pattern in numeration_patterns:
        base_pattern = re_regexp_character_class.sub('1', pattern)
        pattern_list.append((len(base_pattern), pattern))
    pattern_list.sort(key=lambda x: x[0], reverse=True)
    return pattern_list


def create_institute_numeration_group_regexp_pattern(patterns):
    """Using a list of regexp patterns for recognising numeration patterns
       for institute preprint references, ordered by length - longest to
       shortest - create a grouped 'OR' or of these patterns, ready to be
       used in a bigger regexp.
       @param patterns: (list) of strings. All of the numeration regexp
        patterns for recognising an institute's preprint reference styles.
       @return: (string) a grouped 'OR' regexp pattern of the numeration
        patterns. E.g.:
           (?P<num>[12]\d{3} \d\d\d|\d\d \d\d\d|[A-Za-z] \d\d\d)
    """
    patterns_list = [institute_num_pattern_to_regex(p[1]) for p in patterns]
    grouped_numeration_pattern = u"(?P<numn>%s)" % u'|'.join(patterns_list)
    return grouped_numeration_pattern


def institute_num_pattern_to_regex(pattern):
    """Given a numeration pattern from the institutes preprint report
       numbers KB, convert it to turn it into a regexp string for
       recognising such patterns in a reference line.
       Change:
           \     -> \\
           9     -> \d
           a     -> [A-Za-z]
           v     -> [Vv]  # Tony for arXiv vN
           mm    -> (0[1-9]|1[0-2])
           yy    -> \d{2}
           yyyy  -> [12]\d{3}
           /     -> \/
           s     -> \s*
       @param pattern: (string) a user-defined preprint reference numeration
        pattern.
       @return: (string) the regexp for recognising the pattern.
    """
    simple_replacements = [
        ('9', r'\d'),
        ('w+', r'\w+'),
        ('a', r'[A-Za-z]'),
        ('v', r'[Vv]'),
        ('mm', r'(0[1-9]|1[0-2])'),
        ('yyyy', r'[12]\d{3}'),
        ('yy', r'\d\d'),
        ('s', r'\s*'),
        (r'/', r'\/')]

    # now loop through and carry out the simple replacements:
    for repl in simple_replacements:
        pattern = pattern.replace(repl[0], repl[1])

    # now replace a couple of regexp-like paterns:
    # quoted string with non-quoted version ("hello" with hello);
    # Replace / [abcd ]/ with /( [abcd])?/ :
    pattern = re_extract_quoted_text[0].sub(re_extract_quoted_text[1],
                                            pattern)
    pattern = re_extract_char_class[0].sub(re_extract_char_class[1],
                                           pattern)

    # the pattern has been transformed
    return pattern


def build_reportnum_kb(fpath):
    """Given the path to a knowledge base file containing the details
       of institutes and the patterns that their preprint report
       numbering schemes take, create a dictionary of regexp search
       patterns to recognise these preprint references in reference
       lines, and a dictionary of replacements for non-standard preprint
       categories in these references.

       The knowledge base file should consist only of lines that take one
       of the following 3 formats:

         #####Institute Name####

       (the name of the institute to which the preprint reference patterns
        belong, e.g. '#####LANL#####', surrounded by 5 # on either side.)

         <pattern>

       (numeration patterns for an institute's preprints, surrounded by
        < and >.)

         seek-term       ---   replace-term
       (i.e. a seek phrase on the left hand side, a replace phrase on the
       right hand side, with the two phrases being separated by 3 hyphens.)
       E.g.:
         ASTRO PH        ---astro-ph

       The left-hand side term is a non-standard version of the preprint
       reference category; the right-hand side term is the standard version.

       If the KB file cannot be read from, or an unexpected line is
       encountered in the KB, an error message is output to standard error
       and execution is halted with an error-code 0.

       @param fpath: (string) the path to the knowledge base file.
       @return: (tuple) containing 2 dictionaries. The first contains regexp
        search patterns used to identify preprint references in a line. This
        dictionary is keyed by a tuple containing the line number of the
        pattern in the KB and the non-standard category string.
        E.g.: (3, 'ASTRO PH').
        The second dictionary contains the standardised category string,
        and is keyed by the non-standard category string. E.g.: 'astro-ph'.
    """
    def _add_institute_preprint_patterns(preprint_classifications,
                                         preprint_numeration_ptns,
                                         preprint_reference_search_regexp_patterns,
                                         standardised_preprint_reference_categories,
                                         kb_line_num):
        """For a list of preprint category strings and preprint numeration
           patterns for a given institute, create the regexp patterns for
           each of the preprint types.  Add the regexp patterns to the
           dictionary of search patterns
           (preprint_reference_search_regexp_patterns), keyed by the line
           number of the institute in the KB, and the preprint category
           search string.  Also add the standardised preprint category string
           to another dictionary, keyed by the line number of its position
           in the KB and its non-standardised version.
           @param preprint_classifications: (list) of tuples whereby each tuple
            contains a preprint category search string and the line number of
            the name of institute to which it belongs in the KB.
            E.g.: (45, 'ASTRO PH').
           @param preprint_numeration_ptns: (list) of preprint reference
            numeration search patterns (strings)
           @param preprint_reference_search_regexp_patterns: (dictionary) of
            regexp patterns used to search in document lines.
           @param standardised_preprint_reference_categories: (dictionary)
            containing the standardised strings for preprint reference
            categories. (E.g. 'astro-ph'.)
           @param kb_line_num: (integer) - the line number int the KB at
            which a given institute name was found.
           @return: None
        """
        if preprint_classifications and preprint_numeration_ptns:
            # the previous institute had both numeration styles and categories
            # for preprint references.
            # build regexps and add them for this institute:
            # First, order the numeration styles by line-length, and build a
            # grouped regexp for recognising numeration:
            ordered_patterns = \
                order_reportnum_patterns_bylen(preprint_numeration_ptns)
            # create a grouped regexp for numeration part of
            # preprint reference:
            numeration_regexp = \
                create_institute_numeration_group_regexp_pattern(
                    ordered_patterns)

            # for each "classification" part of preprint references, create a
            # complete regex:
            # will be in the style "(categ)-(numatn1|numatn2|numatn3|...)"
            for classification in preprint_classifications:
                search_pattern_str = r'(?:^|[^a-zA-Z0-9\/\.\-])([\[\(]?(?P<categ>' \
                                     + classification[0].strip() + u')' \
                                     + numeration_regexp + r'[\]\)]?)'

                re_search_pattern = re.compile(search_pattern_str,
                                               re.UNICODE)
                preprint_reference_search_regexp_patterns[(kb_line_num,
                                                           classification[0])] =\
                    re_search_pattern
                standardised_preprint_reference_categories[(kb_line_num,
                                                            classification[0])] =\
                    classification[1]

    preprint_reference_search_regexp_patterns = {}  # a dictionary of patterns
    # used to recognise
    # categories of preprints
    # as used by various
    # institutes
    standardised_preprint_reference_categories = {}  # dictionary of
    # standardised category
    # strings for preprint cats
    current_institute_preprint_classifications = []  # list of tuples containing
    # preprint categories in
    # their raw & standardised
    # forms, as read from KB
    current_institute_numerations = []               # list of preprint
    # numeration patterns, as
    # read from the KB

    # pattern to recognise an institute name line in the KB
    re_institute_name = re.compile(r'^\*{5}\s*(.+)\s*\*{5}$', re.UNICODE)

    # pattern to recognise an institute preprint categ line in the KB
    re_preprint_classification = \
        re.compile(r'^\s*(\w.*)\s*---\s*(\w.*)\s*$', re.UNICODE)

    # pattern to recognise a preprint numeration-style line in KB
    re_numeration_pattern = re.compile(r'^\<(.+)\>$', re.UNICODE)

    kb_line_num = 0    # when making the dictionary of patterns, which is
    # keyed by the category search string, this counter
    # will ensure that patterns in the dictionary are not
    # overwritten if 2 institutes have the same category
    # styles.
    with file_resolving(fpath) as fh:
        for rawline in fh:
            if rawline.startswith('#'):
                continue

            kb_line_num += 1
            m_institute_name = re_institute_name.search(rawline)
            if m_institute_name:
                # This KB line is the name of an institute
                # append the last institute's pattern list to the list of
                # institutes:
                _add_institute_preprint_patterns(current_institute_preprint_classifications,
                                                 current_institute_numerations,
                                                 preprint_reference_search_regexp_patterns,
                                                 standardised_preprint_reference_categories,
                                                 kb_line_num)

                # Now start a new dictionary to contain the search patterns
                # for this institute:
                current_institute_preprint_classifications = []
                current_institute_numerations = []
                # move on to the next line
                continue

            m_preprint_classification = \
                re_preprint_classification.search(rawline)
            if m_preprint_classification:
                # This KB line contains a preprint classification for
                # the current institute
                with contextlib.suppress(AttributeError, NameError):
                    current_institute_preprint_classifications.append((m_preprint_classification.group(1),
                                                                       m_preprint_classification.group(2)))
                continue

            m_numeration_pattern = re_numeration_pattern.search(rawline)
            if m_numeration_pattern:
                # This KB line contains a preprint item numeration pattern
                # for the current institute
                with contextlib.suppress(AttributeError, NameError):
                    current_institute_numerations.append(
                        m_numeration_pattern.group(1))
                continue

        _add_institute_preprint_patterns(current_institute_preprint_classifications,
                                         current_institute_numerations,
                                         preprint_reference_search_regexp_patterns,
                                         standardised_preprint_reference_categories,
                                         kb_line_num)

    # return the preprint reference patterns and the replacement strings
    # for non-standard categ-strings:
    return (preprint_reference_search_regexp_patterns,
            standardised_preprint_reference_categories)


def build_special_journals_kb(fpath):
    """Load special journals database from file

    Special journals are journals that have a volume which is not unique
    among different years. To keep the volume unique we are adding the year
    before the volume.
    """
    journals = set()
    with file_resolving(fpath) as fh:
        for line in fh:
            # Skip commented lines
            if line.startswith('#'):
                continue
            # Skip empty line
            if not line.strip():
                continue
            journals.add(line.strip())

    return journals


def build_books_kb(fpath):
    with file_resolving(fpath, reader=csv.reader) as fh:
        books = {}
        for line in fh:
            books[line[1].upper()] = line

    return books


def build_publishers_kb(fpath):
    with file_resolving(fpath, reader=csv.reader, lineterminator='\n') as fh:
        publishers = {}
        for line in fh:
            pattern = re.compile(r'(\b|^)%s(\b|$)' % line[0], re.I | re.U)
            publishers[line[0]] = {'pattern': pattern, 'repl': line[1]}

    return publishers


def build_authors_kb(fpath):
    replacements = []
    with file_resolving(fpath) as fh:
        for rawline in fh:
            if rawline.startswith('#'):
                continue

            # Extract the seek->replace terms from this KB line:
            m_kb_line = re_kb_line.search(rawline)
            if m_kb_line:
                seek = m_kb_line.group('seek')
                repl = m_kb_line.group('repl')
                replacements.append((seek, repl))

    return replacements


def build_journals_re_kb(fpath):
    """Load journals regexps knowledge base

    @see build_journals_kb
    """
    def make_tuple(match):
        regexp = match.group('seek')
        repl = match.group('repl')
        return regexp, repl

    kb = []

    with file_resolving(fpath) as fh:
        for rawline in fh:
            if rawline.startswith('#'):
                continue
            # Extract the seek->replace terms from this KB line:
            m_kb_line = re_kb_line.search(rawline)
            kb.append(make_tuple(m_kb_line))

    return kb


def load_kb_from_iterable(kb, builder):
    return builder(kb)


def load_kb_from_file(path, builder):

    def lazy_parser(fh):
        for rawline in fh:
            if rawline.startswith('#'):
                continue
            rawline = rawline.rstrip("\n")
            # Test line to ensure that it is a correctly formatted
            # knowledge base line:
            # Extract the seek->replace terms from this KB line
            m_kb_line = re_kb_line.search(rawline)
            if m_kb_line:  # good KB line
                yield m_kb_line.group('seek'), m_kb_line.group('repl')
            else:
                raise ValueError("Badly formatted kb '%s' at line %s" % (path, rawline))

    with file_resolving(path) as fh:
        return builder(lazy_parser(fh))


def build_journals_kb(knowledgebase):
    """Given the path to a knowledge base file, read in the contents
       of that file into a dictionary of search->replace word phrases.
       The search phrases are compiled into a regex pattern object.
       The knowledge base file should consist only of lines that take
       the following format:
         seek-term       ---   replace-term
       (i.e. a seek phrase on the left hand side, a replace phrase on
       the right hand side, with the two phrases being separated by 3
       hyphens.) E.g.:
         ASTRONOMY AND ASTROPHYSICS              ---Astron. Astrophys.

       The left-hand side term is a non-standard version of the title,
       whereas the right-hand side term is the standard version.
       If the KB file cannot be read from, or an unexpected line is
       encountered in the KB, an error
       message is output to standard error and execution is halted with
       an error-code 0.

       @param fpath: (string) the path to the knowledge base file.
       @return: (tuple) containing a list and a dictionary. The list
        contains compiled regex patterns used as search terms and will
        be used to force searching order to match that of the knowledge
        base.
        The dictionary contains the search->replace terms.  The keys of
        the dictionary are the compiled regex word phrases used for
        searching in the reference lines; The values in the dictionary are
        the replace terms for matches.
    """
    # Initialise vars:
    # dictionary of search and replace phrases from KB:
    kb = {}
    standardised_titles = {}
    seek_phrases = []
    # A dictionary of "replacement terms" (RHS) to be inserted into KB as
    # "seek terms" later, if they were not already explicitly added
    # by the KB:
    repl_terms = {}
    for seek_phrase, repl in knowledgebase:
        # We match on a simplified line, thus dots are replaced
        # with spaces
        seek_phrase = seek_phrase.replace('.', ' ').upper()

        # good KB line
        # Add the 'replacement term' into the dictionary of
        # replacement terms:
        repl_terms[repl] = None

        # add the phrase from the KB if the 'seek' phrase is longer
        # compile the seek phrase into a pattern:
        seek_ptn = re.compile(r'(?<!\w)(%s)\W' % re.escape(seek_phrase),
                              re.UNICODE)

        kb[seek_phrase] = seek_ptn
        standardised_titles[seek_phrase] = repl
        seek_phrases.append(seek_phrase)

    # Now, for every 'replacement term' found in the KB, if it is
    # not already in the KB as a "search term", add it:
    for repl_term in repl_terms:
        raw_repl_phrase = repl_term.upper()
        raw_repl_phrase = re_punctuation.sub(u' ', raw_repl_phrase)
        raw_repl_phrase = \
            re_group_captured_multiple_space.sub(u' ', raw_repl_phrase)
        raw_repl_phrase = raw_repl_phrase.strip()
        if raw_repl_phrase not in kb:
            # The replace-phrase was not in the KB as a seek phrase
            # It should be added.
            pattern = r'(?<!\/)\b(%s)[^A-Z0-9]' % re.escape(raw_repl_phrase)
            seek_ptn = re.compile(pattern, re.U)
            kb[raw_repl_phrase] = seek_ptn
            standardised_titles[raw_repl_phrase] = repl_term
            seek_phrases.append(raw_repl_phrase)

    # Sort the titles by string length (long - short)
    seek_phrases.sort(key=len, reverse=True)

    # return the raw knowledge base:
    return kb, standardised_titles, seek_phrases


def build_collaborations_kb(knowledgebase):
    kb = {}
    for pattern, collab in knowledgebase:
        prefix = r"(?:^|[\(\"\[\s]|(?<=\W))\s*(?:(?:the|and)\s+)?"
        collaboration_pattern = r"(?:\s*coll(?:aborations?|\.)?)?"
        suffix = r"(?=$|[><\]\)\"\s.,:])"
        pattern = pattern.replace(' ', r'\s')
        pattern = pattern.replace('Collaboration', collaboration_pattern)
        re_pattern = "%s(%s)%s" % (prefix, pattern, suffix)
        kb[collab] = re.compile(re_pattern, re.I | re.U)

    return kb
