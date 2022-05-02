# -*- coding: utf-8 -*-
#
# This file is part of refextract.
# Copyright (C) 2013, 2015, 2016, 2018, 2020 CERN.
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

"""
When a document is converted to plain-text from PDF,
certain characters may result in the plain-text, that are
either unwanted, or broken. These characters need to be corrected
or removed. Examples are, certain control characters that would
be illegal in XML and must be removed; TeX ligatures (etc); broken
accents such as umlauts on letters that must be corrected.
This function returns a dictionary of (unwanted) characters to look
for and the characters that should be used to replace them.
@return: (dictionary) - { seek -> replace, } or charsacters to
replace in plain-text.
"""

import logging
import os
import re
import subprocess

from ..references.config import CFG_PATH_PDFTOTEXT

LOGGER = logging.getLogger(__name__)


def convert_PDF_to_plaintext(fpath, keep_layout=False):
    """ Convert PDF to txt using pdftotext

    Take the path to a PDF file and run pdftotext for this file, capturing
    the output.
    @param fpath: (string) path to the PDF file
    @return: (list) of unicode strings (contents of the PDF file translated
    into plaintext; each string is a line in the document.)
    """
    if not os.path.isfile(CFG_PATH_PDFTOTEXT):
        raise IOError('Missing pdftotext executable')

    if keep_layout:
        layout_option = "-layout"
    else:
        layout_option = "-raw"
    doclines = []
    # Pattern to check for lines with a leading page-break character.
    # If this pattern is matched, we want to split the page-break into
    # its own line because we rely upon this for trying to strip headers
    # and footers, and for some other pattern matching.
    p_break_in_line = re.compile(r'^\s*\f(.+)$', re.UNICODE)
    # build pdftotext command:
    cmd_pdftotext = [CFG_PATH_PDFTOTEXT, layout_option, "-q",
                     "-enc", "UTF-8", fpath, "-"]

    LOGGER.debug(u"%s", ' '.join(cmd_pdftotext))
    # open pipe to pdftotext:
    pipe_pdftotext = subprocess.Popen(cmd_pdftotext, stdout=subprocess.PIPE)
    # read back results:
    for docline in pipe_pdftotext.stdout:
        unicodeline = docline.decode("utf-8")
        # Check for a page-break in this line:
        m_break_in_line = p_break_in_line.match(unicodeline)
        if m_break_in_line is None:
            # There was no page-break in this line. Just add the line:
            doclines.append(unicodeline)
        else:
            # If there was a page-break character in the same line as some
            # text, split it out into its own line so that we can later
            # try to find headers and footers:
            doclines.append(u"\f")
            doclines.append(m_break_in_line.group(1))

    LOGGER.debug(u"convert_PDF_to_plaintext found: %s lines of text", len(doclines))

    return doclines
