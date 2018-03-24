# -*- coding: utf-8 -*-
#
# This file is part of refextract.
# Copyright (C) 2016, 2018 CERN.
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

import os

import pytest


@pytest.fixture
def pdf_files():
    path_to_pdfs = os.path.join(os.path.dirname(__file__), 'data')
    pdfs = os.listdir(path_to_pdfs)
    pdfs.sort()
    return [os.path.join(path_to_pdfs, pdf) for pdf in pdfs]
