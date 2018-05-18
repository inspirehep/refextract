# -*- coding: utf-8 -*-
#
# This file is part of refextract
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

from refextract.references.pdf import (
    extract_texkeys_from_pdf
)


def test_extract_texkeys_from_pdf(pdf_files):
    one_col_keys = extract_texkeys_from_pdf(pdf_files[0])
    expected = [
        u'Englert:1964et',
        u'Higgs:1964ia',
        u'Higgs:1964pj',
        u'Guralnik:1964eu',
        u'Higgs:1966ev',
        u'Kibble:1967sv',
        u'HiggsObservationATLAS',
        u'HiggsObservationCMS',
        u'CMSLong2013',
        u'atlas_coupling_paper',
        u'atlas_spin_paper',
        u'CMS_combination',
        u'Khachatryan:2014kca',
        u'atlas_mass_paper',
        u'CMS_Hgg',
        u'CMS_HZZ',
        u'Baak:2014ora',
        u'Dixon:2003yb',
        u'Martin:2012xc',
        u'Dixon:2013haa',
        u'Kauer:2012hd',
        u'ATLAS',
        u'CMS',
        u'atlas_hgg_coupling',
        u'LHC-HCG',
        u'Cowan:2010st',
        u'Verkerke:2003ir',
        u'Moneta:2010pm',
        u'Cranmer:2012sba',
        u'Aad:2014nim',
        u'Aad:2014rra',
        u'Chatrchyan:2012xi',
        u'Khachatryan:2015hwa',
        u'Khachatryan:2015iwa',
        u'Dauncey:2014xga',
        u'Z-Pole'
    ]
    assert one_col_keys == expected

    two_col_keys = extract_texkeys_from_pdf(pdf_files[1])
    expected = [
        u'Aad:2015owa',
        u'CMSCollaboration:2014df',
        u'Fukano:2015ud',
        u'Hisano:2015gna',
        u'Franzosi:2015ts',
        u'Cheung:2015vl',
        u'Dobrescu:2015va',
        u'AguilarSaavedra:2015tw',
        u'Alves:2015tf',
        u'Gao:2015ws',
        u'Thamm:2015wd',
        u'Brehmer:2015tq',
        u'Cao:2015we',
        u'Cacciapaglia:2015uf',
        u'Anonymous:2015ul',
        u'Abe:2015ud',
        u'Carmona:2015vx',
        u'Allanach:2015tr',
        u'Chiang:2015up',
        u'Cacciapaglia:2015vk',
        u'Fukano:2015vk',
        u'Sanz:2015tp',
        u'Chen:2015wa',
        u'Omura:2015vz',
        u'Chao:2015up',
        u'Anchordoqui:2015gb',
        u'Bian:2015tv',
        u'Kim:2015vl',
        u'Lane:2015wm',
        u'Faraggi:2015vi',
        u'Low:2015tn',
        u'Liew:2015to',
        u'Terazawa:2015ul',
        u'Arnan:2015vi',
        u'Niehoff:2015vw',
        u'Fichet:2015wf',
        u'Goncalves:2015ul',
        u'ATLAScollaboration:2014tl',
        u'Perazzi:2000ku',
        u'Perazzi:2000dk',
        u'Gorbunov:2002co',
        u'Antoniadis:2011ve',
        u'Bertolini:2011wj',
        u'Petersson:2011in',
        u'Bellazzini:2012ul',
        u'Antoniadis:2012ui',
        u'2013PhRvD..87a3008P',
        u'Dudas:2012ti',
        u'Dudas:2013tc',
        u'ATLAScollaboration:2015uw',
        u'CMSCollaboration:2014ke',
        u'ATLAScollaboration:2015ue',
        u'ATLAScollaboration:2014ur'
    ]
    assert two_col_keys == expected


def test_extract_texkeys_from_pdf_no_crash_on_incomplete_dest_coordinates(
        pdf_files):
    expected = []
    result = extract_texkeys_from_pdf(pdf_files[2])

    assert result == expected


def test_extract_texkeys_from_pdf_no_crash_on_pydpf2_error(pdf_files):
    expected = []
    result = extract_texkeys_from_pdf(pdf_files[3])

    assert result == expected


def test_extract_texkeys_from_pdf_no_crash_on_other_exceptions(pdf_files):
    expected = []
    result = extract_texkeys_from_pdf(pdf_files[5])

    assert result == expected
