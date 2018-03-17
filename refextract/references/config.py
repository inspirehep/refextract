# -*- coding: utf-8 -*-
#
# This file is part of refextract.
# Copyright (C) 2013, 2015, 2017, 2018 CERN.
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

"""refextract configuration."""

from __future__ import absolute_import, division, print_function

import os

try:
    from shutil import which
except ImportError:
    # CPython <3.3
    from distutils.spawn import find_executable as which

import pkg_resources

# Version number:
CFG_PATH_PDFTOTEXT = os.environ.get('CFG_PATH_PDFTOTEXT', which('pdftotext'))

# Module config directory
CFG_KBS_DIR = pkg_resources.resource_filename('refextract.references', 'kbs')

CFG_REFEXTRACT_KBS = {
    'journals': "%s/journal-titles.kb" % CFG_KBS_DIR,
    'journals-re': "%s/journal-titles-re.kb" % CFG_KBS_DIR,
    'report-numbers': "%s/report-numbers.kb" % CFG_KBS_DIR,
    'authors': "%s/authors.kb" % CFG_KBS_DIR,
    'collaborations': "%s/collaborations.kb" % CFG_KBS_DIR,
    'books': "%s/books.kb" % CFG_KBS_DIR,
    'conferences': "%s/conferences.kb" % CFG_KBS_DIR,
    'publishers': "%s/publishers.kb" % CFG_KBS_DIR,
    'special-journals': "%s/special-journals.kb" % CFG_KBS_DIR,
}

# Reference fields:
CFG_REFEXTRACT_FIELDS = {
    'misc': 'm',
    'linemarker': 'o',
    'doi': 'a',
    'hdl': 'a',
    'reportnumber': 'r',
    'journal': 's',
    'url': 'u',
    'urldesc': 'z',
    'author': 'h',
    'title': 't',
    'isbn': 'i',
    'publisher': 'p',
    'year': 'y',
    'collaboration': 'c',
    'recid': '0',
}

# Internal tags are used by refextract to mark-up recognised citation
# information.
CFG_REFEXTRACT_MARKER_OPENING_REPORT_NUM = r"<cds.REPORTNUMBER>"
CFG_REFEXTRACT_MARKER_OPENING_TITLE = r"<cds.JOURNAL>"
CFG_REFEXTRACT_MARKER_OPENING_TITLE_IBID = r"<cds.JOURNALibid>"
CFG_REFEXTRACT_MARKER_OPENING_SERIES = r"<cds.SER>"
CFG_REFEXTRACT_MARKER_OPENING_VOLUME = r"<cds.VOL>"
CFG_REFEXTRACT_MARKER_OPENING_YEAR = r"<cds.YR>"
CFG_REFEXTRACT_MARKER_OPENING_PAGE = r"<cds.PG>"
CFG_REFEXTRACT_MARKER_OPENING_QUOTED = r"<cds.QUOTED>"
CFG_REFEXTRACT_MARKER_OPENING_ISBN = r"<cds.ISBN>"
CFG_REFEXTRACT_MARKER_OPENING_PUBLISHER = r"<cds.PUBLISHER>"
CFG_REFEXTRACT_MARKER_OPENING_COLLABORATION = r"<cds.COLLABORATION>"

# These are the "closing tags:
CFG_REFEXTRACT_MARKER_CLOSING_REPORT_NUM = r"</cds.REPORTNUMBER>"
CFG_REFEXTRACT_MARKER_CLOSING_TITLE = r"</cds.JOURNAL>"
CFG_REFEXTRACT_MARKER_CLOSING_TITLE_IBID = r"</cds.JOURNALibid>"
CFG_REFEXTRACT_MARKER_CLOSING_SERIES = r"</cds.SER>"
CFG_REFEXTRACT_MARKER_CLOSING_VOLUME = r"</cds.VOL>"
CFG_REFEXTRACT_MARKER_CLOSING_YEAR = r"</cds.YR>"
CFG_REFEXTRACT_MARKER_CLOSING_PAGE = r"</cds.PG>"
CFG_REFEXTRACT_MARKER_CLOSING_QUOTED = r"</cds.QUOTED>"
CFG_REFEXTRACT_MARKER_CLOSING_ISBN = r"</cds.ISBN>"
CFG_REFEXTRACT_MARKER_CLOSING_PUBLISHER = r"</cds.PUBLISHER>"
CFG_REFEXTRACT_MARKER_CLOSING_COLLABORATION = r"</cds.COLLABORATION>"

# Of the form '</cds.AUTHxxxx>' only
CFG_REFEXTRACT_MARKER_CLOSING_AUTHOR_STND = r"</cds.AUTHstnd>"
CFG_REFEXTRACT_MARKER_CLOSING_AUTHOR_ETAL = r"</cds.AUTHetal>"
CFG_REFEXTRACT_MARKER_CLOSING_AUTHOR_INCL = r"</cds.AUTHincl>"

# The minimum length of a reference's misc text to be deemed insignificant.
# when comparing misc text with semi-colon defined sub-references.
# Values higher than this value reflect meaningful misc text.
# Hence, upon finding a correct semi-colon, but having current misc text
# length less than this value (without other meaningful reference objects:
# report numbers, titles...) then no split will occur.
# (A higher value will increase splitting strictness. i.e. Fewer splits)
CGF_REFEXTRACT_SEMI_COLON_MISC_TEXT_SENSITIVITY = 60

# The length of misc text between two adjacent authors which is
# deemed as insignificant. As such, when misc text of a length less
# than this value is found, then the latter author group is dumped into misc.
# (A higher value will increase splitting strictness. i.e. Fewer splits)
CGF_REFEXTRACT_ADJACENT_AUTH_MISC_SEPARATION = 10

# Maximum number of lines for a citation before it is considered invalid
CFG_REFEXTRACT_MAX_LINES = 25
