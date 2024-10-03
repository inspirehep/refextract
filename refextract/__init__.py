# -*- coding: utf-8 -*-
#
# This file is part of refextract.
# Copyright (C) 2015, 2016, 2018, 2020 CERN.
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

"""Refextract."""

from refextract.references.api import (
    extract_journal_reference,
    extract_references_from_file,
    extract_references_from_string,
    extract_references_from_url,
)

__all__ = (
    "extract_journal_reference",
    "extract_references_from_file",
    "extract_references_from_string",
    "extract_references_from_url",
)
