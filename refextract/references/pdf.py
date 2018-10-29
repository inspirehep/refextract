# -*- coding: utf-8 -*-
#
# This file is part of refextract.
# Copyright (C) 2016, 2017, 2018 CERN.
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

import logging

from PyPDF2 import PdfFileReader

from .regexs import re_reference_in_dest


LOGGER = logging.getLogger(__name__)


class IncompleteCoordinatesError(Exception):
    """Exception raised when a named destination does not have all required
    coordinates.
    """
    pass


def extract_texkeys_from_pdf(pdf_file):
    """
    Extract the texkeys from the given PDF file

    This is done by looking up the named destinations in the PDF

    @param pdf_file: path to a PDF

    @return: list of all texkeys found in the PDF
    """
    with open(pdf_file, 'rb') as pdf_stream:
        try:
            pdf = PdfFileReader(pdf_stream, strict=False)
            destinations = pdf.getNamedDestinations()
        except Exception:
            LOGGER.debug(u"PDF: Internal PyPDF2 error, no TeXkeys returned.")
            return []
        # not all named destinations point to references
        refs = [dest for dest in destinations.iteritems()
                if re_reference_in_dest.match(dest[0])]
        try:
            if _destinations_in_two_columns(pdf, refs):
                LOGGER.debug(u"PDF: Using two-column layout")

                def sortfunc(dest_couple):
                    return _destination_position(pdf, dest_couple[1])

            else:
                LOGGER.debug(u"PDF: Using single-column layout")

                def sortfunc(dest_couple):
                    (page, _, ypos, xpos) = _destination_position(
                        pdf, dest_couple[1])
                    return (page, ypos, xpos)

            refs.sort(key=sortfunc)
            # extract the TeXkey from the named destination name
            return [re_reference_in_dest.match(destname).group(1)
                    for (destname, _) in refs]
        except Exception:
            LOGGER.debug(u"PDF: Impossible to determine layout, no TeXkeys returned")
            return []


def _destinations_in_two_columns(pdf, destinations, cutoff=3):
    """
    Check if the named destinations are organized along two columns (heuristic)

    @param pdf: a PdfFileReader object
    @param destinations:

    'cutoff' is used to tune the heuristic: if 'cutoff' destinations in the
    would-be second column start at the same position, return True
    """
    # iterator for the x coordinates of refs in the would-be second column
    xpositions = (_destination_position(pdf, dest)[3] for (_, dest)
                  in destinations
                  if _destination_position(pdf, dest)[1] == 1)
    xpos_count = {}
    for xpos in xpositions:
        xpos_count[xpos] = xpos_count.get(xpos, 0) + 1
        if xpos_count[xpos] >= cutoff:
            return True
    return False


def _destination_position(pdf, destination):
    """
    Gives a tuple (page, column, -y, x) representing the position of the
    NamedDestination

    This representation is useful for sorting named destinations and
    assumes the text has at most 2 columns
    """
    pagewidth = pdf.getPage(
        pdf.getDestinationPageNumber(destination)
    ).cropBox.lowerRight[0]
    if not destination.left or not destination.top:
        raise IncompleteCoordinatesError(destination)
    # assuming max 2 columns
    column = (2 * destination.left) // pagewidth
    return (pdf.getDestinationPageNumber(destination),
            column, -destination.top, destination.left)
