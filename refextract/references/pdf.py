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


def extract_texkeys_and_urls_from_pdf(pdf_file):
    """
    Extract the texkeys and corresponding urls from the given PDF file

    This is done by looking up the named destinations in the PDF

    @param pdf_file: path to a PDF

    @return: list of dictionaries with all texkeys and corresponding urls found in the PDF
    """
    with open(pdf_file, "rb") as pdf_stream:
        try:
            pdf = PdfFileReader(pdf_stream, strict=False)
            destinations = pdf.getNamedDestinations()
            urls = extract_urls(pdf)
        except Exception:
            LOGGER.debug(u"PDF: Internal PyPDF2 error, no TeXkeys returned.")
            return []
        # not all named destinations point to references
        refs = [
            dest for dest in destinations.items() if re_reference_in_dest.match(dest[0])
        ]
        try:
            if _destinations_in_two_columns(pdf, refs):
                LOGGER.debug(u"PDF: Using two-column layout")

                def sortfunc(dest_couple):
                    return dest_couple[1]

            else:
                LOGGER.debug(u"PDF: Using single-column layout")

                def sortfunc(dest_couple):
                    page, _, ypos, xpos = dest_couple[1]
                    return (page, ypos, xpos)

            refs = [(dest[0], _destination_position(pdf, dest[1])) for dest in refs]
            refs.sort(key=sortfunc)
            urls = [(uri["/A"]["/URI"], _uri_position(pdf, uri)) for uri in urls]
            urls.sort(key=sortfunc)
            texkey_url_list = []
            for nb, ref in enumerate(refs):
                current_texkey_urls_dict = {}
                current_texkey_urls_dict["texkey"] = re_reference_in_dest.match(
                    ref[0]
                ).group(1)
                if nb < len(refs) - 1:
                    next_reference_data = refs[nb + 1]
                    matched_urls_for_reference, urls = _match_urls_with_reference(
                        urls, ref, next_reference_data
                    )
                else:
                    matched_urls_for_reference, urls = _match_urls_with_reference(urls, ref)
                if matched_urls_for_reference:
                    current_texkey_urls_dict["urls"] = matched_urls_for_reference
                texkey_url_list.append(current_texkey_urls_dict)
            return texkey_url_list
        except Exception:
            LOGGER.debug(u"PDF: Impossible to determine layout, no TeXkeys returned")
            return []


def _match_urls_with_reference(urls_to_match, reference, next_reference=None):
    ref_page_number, ref_column, ref_y, _ = reference[1]
    if next_reference:
        next_ref_page_number, next_ref_col, next_ref_y, _ = next_reference[1]
    urls_for_reference = set()
    for (url_index, url) in enumerate(urls_to_match):
        url_page_number, _, url_y, _ = url[1]
        is_url_under_texkey = ref_y <= url_y
        is_reference_on_same_page_as_url = ref_page_number == url_page_number
        is_reference_on_previous_page_than_url = ref_page_number + 1 == url_page_number
        if (
            not next_reference and (
                is_reference_on_same_page_as_url or
                is_reference_on_previous_page_than_url
            ) and
            is_url_under_texkey
        ):
            urls_for_reference.add(url[0])
            continue
        is_url_between_texkeys = (
            is_reference_on_same_page_as_url or is_reference_on_previous_page_than_url
        ) and (ref_y <= url_y <= next_ref_y)
        is_last_reference_in_page = (
            is_reference_on_same_page_as_url and
            (next_ref_page_number > url_page_number) and
            is_url_under_texkey
        )
        is_in_new_column = (
            is_reference_on_same_page_as_url and
            (next_ref_page_number == url_page_number) and
            is_url_under_texkey and
            (next_ref_col > ref_column)
        )
        is_url_unrelated_to_references = ref_page_number > url_page_number
        is_url_for_next_reference = url_y >= next_ref_y
        if is_url_between_texkeys:
            urls_for_reference.add(url[0])
        elif is_last_reference_in_page:
            urls_for_reference.add(url[0])
        elif is_in_new_column:
            urls_for_reference.add(url[0])
        elif is_url_unrelated_to_references:
            continue
        elif is_url_for_next_reference:
            urls_to_match = urls_to_match[url_index:]
            break
    if not next_reference:
        urls_to_match = []
    return urls_for_reference, urls_to_match


def _destinations_in_two_columns(pdf, destinations, cutoff=3):
    """
    Check if the named destinations are organized along two columns (heuristic)

    @param pdf: a PdfFileReader object
    @param destinations:

    'cutoff' is used to tune the heuristic: if 'cutoff' destinations in the
    would-be second column start at the same position, return True
    """
    # iterator for the x coordinates of refs in the would-be second column
    xpositions = (
        _destination_position(pdf, dest)[3]
        for (_, dest) in destinations
        if _destination_position(pdf, dest)[1] == 1
    )
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
    return (
        pdf.getDestinationPageNumber(destination),
        column,
        -destination.top,
        destination.left,
    )


def _uri_position(pdf, uri_destination):
    """
    Gives a tuple (page, column, -y, x) representing the position of the URI
    """
    page_nb = uri_destination.get("page_nb")
    destintation_left = uri_destination["/Rect"][0]
    destintation_top = uri_destination["/Rect"][3]
    pagewidth = pdf.getPage(page_nb).cropBox.lowerRight[0]
    column = (2 * destintation_left) // pagewidth
    # neccessary to exclude column from sorting
    return (page_nb, column, -destintation_top, destintation_left)


def extract_urls(pdf):
    urls = []
    pages = pdf.getNumPages()
    for page_nb in range(pages):
        page = pdf.getPage(page_nb)
        page_object = page.getObject()
        urls_for_page = _get_urls_data_from_page_object(page_object, page_nb)
        urls.extend(urls_for_page)
    return urls


def _get_urls_data_from_page_object(page_object, page_nb):
    urls_at_page = []
    annotations = page_object.get("/Annots", [])
    for annotation in annotations:
        annotation_object = annotation.getObject()
        if "/URI" in annotation_object["/A"]:
            annotation_object.update({"page_nb": page_nb})
            urls_at_page.append(annotation_object)
    return urls_at_page
