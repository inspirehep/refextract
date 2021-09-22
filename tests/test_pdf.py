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

from refextract.references.pdf import extract_texkeys_and_urls_from_pdf


def test_extract_texkeys_and_urls_from_pdf(pdf_files):
    one_col_keys = extract_texkeys_and_urls_from_pdf(pdf_files[0])
    expected = [
        {
            "texkey": "Englert:1964et",
            "urls": {"http://dx.doi.org/10.1103/PhysRevLett.13.321"},
        },
        {
            "texkey": "Higgs:1964ia",
            "urls": {"http://dx.doi.org/10.1016/0031-9163(64)91136-9"},
        },
        {
            "texkey": "Higgs:1964pj",
            "urls": {"http://dx.doi.org/10.1103/PhysRevLett.13.508"},
        },
        {
            "texkey": "Guralnik:1964eu",
            "urls": {"http://dx.doi.org/10.1103/PhysRevLett.13.585"},
        },
        {
            "texkey": "Higgs:1966ev",
            "urls": {"http://dx.doi.org/10.1103/PhysRev.145.1156"},
        },
        {
            "texkey": "Kibble:1967sv",
            "urls": {"http://dx.doi.org/10.1103/PhysRev.155.1554"},
        },
        {
            "texkey": "HiggsObservationATLAS",
            "urls": {
                "http://dx.doi.org/10.1016/j.physletb.2012.08.020",
                "http://www.arXiv.org/abs/1207.7214",
            },
        },
        {
            "texkey": "HiggsObservationCMS",
            "urls": {
                "http://dx.doi.org/10.1016/j.physletb.2012.08.021",
                "http://www.arXiv.org/abs/1207.7235",
            },
        },
        {
            "texkey": "CMSLong2013",
            "urls": {
                "http://dx.doi.org/10.1007/JHEP06(2013)081",
                "http://www.arXiv.org/abs/1303.4571",
            },
        },
        {
            "texkey": "atlas_coupling_paper",
            "urls": {
                "http://dx.doi.org/10.1016/j.physletb.2013.08.010",
                "http://www.arXiv.org/abs/1307.1427",
            },
        },
        {
            "texkey": "atlas_spin_paper",
            "urls": {
                "http://dx.doi.org/10.1016/j.physletb.2013.08.026",
                "http://www.arXiv.org/abs/1307.1432",
                "http://www.arXiv.org/abs/1307.1432",
            },
        },
        {"texkey": "CMS_combination", "urls": {"http://www.arXiv.org/abs/1412.8662"}},
        {
            "texkey": "Khachatryan:2014kca",
            "urls": {"http://www.arXiv.org/abs/1411.3441"},
        },
        {
            "texkey": "atlas_mass_paper",
            "urls": {
                "http://dx.doi.org/10.1103/PhysRevD.90.052004",
                "http://www.arXiv.org/abs/1406.3827",
            },
        },
        {
            "texkey": "CMS_Hgg",
            "urls": {
                "http://dx.doi.org/10.1140/epjc/s10052-014-3076-z",
                "http://www.arXiv.org/abs/1407.0558",
            },
        },
        {
            "texkey": "CMS_HZZ",
            "urls": {
                "http://dx.doi.org/10.1103/PhysRevD.89.092007",
                "http://www.arXiv.org/abs/1312.5353",
                "http://www.arXiv.org/abs/1312.5353",
            },
        },
        {
            "texkey": "Baak:2014ora",
            "urls": {
                "http://dx.doi.org/10.1140/epjc/s10052-014-3046-5",
                "http://www.arXiv.org/abs/1407.3792",
            },
        },
        {
            "texkey": "Dixon:2003yb",
            "urls": {
                "http://dx.doi.org/10.1103/PhysRevLett.90.252001",
                "http://www.arXiv.org/abs/hep-ph/0302233",
            },
        },
        {
            "texkey": "Martin:2012xc",
            "urls": {
                "http://dx.doi.org/10.1103/PhysRevD.86.073016",
                "http://www.arXiv.org/abs/1208.1533",
            },
        },
        {
            "texkey": "Dixon:2013haa",
            "urls": {
                "http://dx.doi.org/10.1103/PhysRevLett.111.111802",
                "http://www.arXiv.org/abs/1305.3854",
            },
        },
        {
            "texkey": "Kauer:2012hd",
            "urls": {
                "http://dx.doi.org/10.1007/JHEP08(2012)116",
                "http://www.arXiv.org/abs/1206.4803",
            },
        },
        {
            "texkey": "ATLAS",
            "urls": {"http://dx.doi.org/10.1088/1748-0221/3/08/S08003"},
        },
        {"texkey": "CMS", "urls": {"http://dx.doi.org/10.1088/1748-0221/3/08/S08004"}},
        {
            "texkey": "atlas_hgg_coupling",
            "urls": {
                "http://dx.doi.org/10.1103/PhysRevD.90.112015",
                "http://www.arXiv.org/abs/1408.7084",
            },
        },
        {"texkey": "LHC-HCG", "urls": {"http://cdsweb.cern.ch/record/1379837"}},
        {
            "texkey": "Cowan:2010st",
            "urls": {
                "http://dx.doi.org/10.1140/epjc/s10052-011-1554-0",
                "http://www.arXiv.org/abs/1007.1727",
            },
        },
        {
            "texkey": "Verkerke:2003ir",
            "urls": {"http://www.arXiv.org/abs/physics/0306116"},
        },
        {
            "texkey": "Moneta:2010pm",
            "urls": {
                "http://www.arXiv.org/abs/1009.1003",
                "http://pos.sissa.it/archive/conferences/093/057/ACAT2010_057.pdf",
            },
        },
        {"texkey": "Cranmer:2012sba"},
        {
            "texkey": "Aad:2014nim",
            "urls": {
                "http://dx.doi.org/10.1140/epjc/s10052-014-3071-4",
                "http://www.arXiv.org/abs/1407.5063",
            },
        },
        {
            "texkey": "Aad:2014rra",
            "urls": {
                "http://dx.doi.org/10.1140/epjc/s10052-014-3130-x",
                "http://www.arXiv.org/abs/1407.3935",
            },
        },
        {
            "texkey": "Chatrchyan:2012xi",
            "urls": {
                "http://dx.doi.org/10.1088/1748-0221/7/10/P10002",
                "http://www.arXiv.org/abs/1206.4071",
            },
        },
        {
            "texkey": "Khachatryan:2015hwa",
            "urls": {"http://www.arXiv.org/abs/1502.02701"},
        },
        {
            "texkey": "Khachatryan:2015iwa",
            "urls": {"http://www.arXiv.org/abs/1502.02702"},
        },
        {"texkey": "Dauncey:2014xga", "urls": {"http://www.arXiv.org/abs/1408.6865"}},
        {
            "texkey": "Z-Pole",
            "urls": {
                "http://dx.doi.org/10.1016/j.physrep.2005.12.006",
                "http://www.arXiv.org/abs/hep-ex/0509008",
            },
        },
    ]
    assert one_col_keys == expected

    two_col_keys = extract_texkeys_and_urls_from_pdf(pdf_files[1])

    expected = [
        {
            "texkey": "Aad:2015owa",
            "urls": {
                "http://arxiv.org/abs/1506.00962",
                "http://inspirehep.net/record/1374218",
            },
        },
        {
            "texkey": "CMSCollaboration:2014df",
            "urls": {
                "http://arxiv.org/abs/1405.1994",
                "http://dx.doi.org/10.1007/JHEP08(2014)173",
                "http://inspirehep.net/record/1294937",
            },
        },
        {
            "texkey": "Fukano:2015ud",
            "urls": {
                "http://arxiv.org/abs/1506.03751",
                "http://inspirehep.net/record/1375823",
            },
        },
        {
            "texkey": "Hisano:2015gna",
            "urls": {
                "http://arxiv.org/abs/1506.03931",
                "http://inspirehep.net/record/1376004",
            },
        },
        {
            "texkey": "Franzosi:2015ts",
            "urls": {
                "http://arxiv.org/abs/1506.04392",
                "http://inspirehep.net/record/1376127",
            },
        },
        {
            "texkey": "Cheung:2015vl",
            "urls": {
                "http://arxiv.org/abs/1506.06064",
                "http://inspirehep.net/record/1377207",
            },
        },
        {
            "texkey": "Dobrescu:2015va",
            "urls": {
                "http://arxiv.org/abs/1506.06736",
                "http://inspirehep.net/record/1377366",
            },
        },
        {
            "texkey": "AguilarSaavedra:2015tw",
            "urls": {
                "http://arxiv.org/abs/1506.06739",
                "http://inspirehep.net/record/1377367",
            },
        },
        {
            "texkey": "Alves:2015tf",
            "urls": {
                "http://arxiv.org/abs/1506.06767",
                "http://inspirehep.net/record/1377544",
            },
        },
        {
            "texkey": "Gao:2015ws",
            "urls": {
                "http://arxiv.org/abs/1506.07511",
                "http://inspirehep.net/record/1377754",
            },
        },
        {
            "texkey": "Thamm:2015wd",
            "urls": {
                "http://arxiv.org/abs/1506.08688",
                "http://inspirehep.net/record/1380186",
            },
        },
        {
            "texkey": "Brehmer:2015tq",
            "urls": {
                "http://arxiv.org/abs/1507.00013",
                "http://inspirehep.net/record/1380602",
            },
        },
        {
            "texkey": "Cao:2015we",
            "urls": {
                "http://arxiv.org/abs/1507.00268",
                "http://inspirehep.net/record/1380611",
            },
        },
        {
            "texkey": "Cacciapaglia:2015uf",
            "urls": {
                "http://arxiv.org/abs/1507.00900",
                "http://inspirehep.net/record/1381176",
            },
        },
        {
            "texkey": "Anonymous:2015ul",
            "urls": {
                "http://arxiv.org/abs/1507.01185",
                "http://inspirehep.net/record/1381519",
            },
        },
        {
            "texkey": "Abe:2015ud",
            "urls": {
                "http://arxiv.org/abs/1507.01681",
                "http://inspirehep.net/record/1381764",
            },
        },
        {
            "texkey": "Carmona:2015vx",
            "urls": {
                "http://arxiv.org/abs/1507.01914",
                "http://inspirehep.net/record/1381767",
            },
        },
        {
            "texkey": "Allanach:2015tr",
            "urls": {
                "http://arxiv.org/abs/1507.01638",
                "http://inspirehep.net/record/1381777",
            },
        },
        {
            "texkey": "Chiang:2015up",
            "urls": {
                "http://arxiv.org/abs/1507.02483",
                "http://inspirehep.net/record/1382171",
            },
        },
        {
            "texkey": "Cacciapaglia:2015vk",
            "urls": {
                "http://arxiv.org/abs/1507.03098",
                "http://inspirehep.net/record/1382589",
            },
        },
        {
            "texkey": "Fukano:2015vk",
            "urls": {
                "http://arxiv.org/abs/1507.03428",
                "http://inspirehep.net/record/1382596",
            },
        },
        {
            "texkey": "Sanz:2015tp",
            "urls": {
                "http://arxiv.org/abs/1507.03553",
                "http://inspirehep.net/record/1382627",
            },
        },
        {
            "texkey": "Chen:2015wa",
            "urls": {
                "http://arxiv.org/abs/1507.04431",
                "http://inspirehep.net/record/1383125",
            },
        },
        {
            "texkey": "Omura:2015vz",
            "urls": {
                "http://arxiv.org/abs/1507.05028",
                "http://inspirehep.net/record/1383681",
            },
        },
        {
            "texkey": "Chao:2015up",
            "urls": {
                "http://arxiv.org/abs/1507.05310",
                "http://inspirehep.net/record/1383880",
            },
        },
        {
            "texkey": "Anchordoqui:2015gb",
            "urls": {
                "http://arxiv.org/abs/1507.05299",
                "http://inspirehep.net/record/1383896",
            },
        },
        {
            "texkey": "Bian:2015tv",
            "urls": {
                "http://arxiv.org/abs/1507.06018",
                "http://inspirehep.net/record/1384280",
            },
        },
        {
            "texkey": "Kim:2015vl",
            "urls": {
                "http://arxiv.org/abs/1507.06312",
                "http://inspirehep.net/record/1384495",
            },
        },
        {
            "texkey": "Lane:2015wm",
            "urls": {
                "http://arxiv.org/abs/1507.07102",
                "http://inspirehep.net/record/1385103",
            },
        },
        {
            "texkey": "Faraggi:2015vi",
            "urls": {
                "http://arxiv.org/abs/1507.07406",
                "http://inspirehep.net/record/1385132",
            },
        },
        {
            "texkey": "Low:2015tn",
            "urls": {
                "http://arxiv.org/abs/1507.07557",
                "http://inspirehep.net/record/1385326",
            },
        },
        {
            "texkey": "Liew:2015to",
            "urls": {
                "http://arxiv.org/abs/1507.08273",
                "http://inspirehep.net/record/1385606",
            },
        },
        {
            "texkey": "Terazawa:2015ul",
            "urls": {
                "http://arxiv.org/abs/1508.00172",
                "http://inspirehep.net/record/1386269",
            },
        },
        {
            "texkey": "Arnan:2015vi",
            "urls": {
                "http://arxiv.org/abs/1508.00174",
                "http://inspirehep.net/record/1386270",
            },
        },
        {
            "texkey": "Niehoff:2015vw",
            "urls": {
                "http://arxiv.org/abs/1508.00569",
                "http://inspirehep.net/record/1386484",
            },
        },
        {
            "texkey": "Fichet:2015wf",
            "urls": {
                "http://arxiv.org/abs/1508.04814",
                "http://inspirehep.net/record/1388736",
            },
        },
        {
            "texkey": "Goncalves:2015ul",
            "urls": {
                "http://arxiv.org/abs/1508.04162",
                "http://inspirehep.net/record/1388372",
            },
        },
        {
            "texkey": "ATLAScollaboration:2014tl",
            "urls": {
                "http://arxiv.org/abs/1407.1376",
                "http://inspirehep.net/record/1305096",
            },
        },
        {
            "texkey": "Perazzi:2000ku",
            "urls": {
                "http://arxiv.org/abs/hep-ph/0001025",
                "http://dx.doi.org/10.1016/S0550-3213(00)00055-9",
                "http://inspirehep.net/record/522761",
            },
        },
        {
            "texkey": "Perazzi:2000dk",
            "urls": {
                "http://arxiv.org/abs/hep-ph/0005076",
                "http://dx.doi.org/10.1016/S0550-3213(00)00504-6",
                "http://inspirehep.net/record/526995",
            },
        },
        {
            "texkey": "Gorbunov:2002co",
            "urls": {
                "http://arxiv.org/abs/hep-ph/0203078",
                "http://dx.doi.org/10.1088/1126-6708/2002/07/043",
                "http://inspirehep.net/record/583867",
            },
        },
        {
            "texkey": "Antoniadis:2011ve",
            "urls": {
                "http://arxiv.org/abs/1110.5939",
                "http://dx.doi.org/10.1016/j.nuclphysb.2011.12.005",
                "http://inspirehep.net/record/943316",
            },
        },
        {
            "texkey": "Bertolini:2011wj",
            "urls": {
                "http://arxiv.org/abs/1111.0628",
                "http://dx.doi.org/10.1007/JHEP04(2012)130",
                "http://inspirehep.net/record/944406",
            },
        },
        {
            "texkey": "Petersson:2011in",
            "urls": {
                "http://arxiv.org/abs/1111.3368",
                "http://dx.doi.org/10.1007/JHEP02(2012)142",
                "http://inspirehep.net/record/945946",
            },
        },
        {
            "texkey": "Bellazzini:2012ul",
            "urls": {
                "http://arxiv.org/abs/1207.0803",
                "http://dx.doi.org/10.1103/PhysRevD.86.033016",
                "http://inspirehep.net/record/1121023",
            },
        },
        {
            "texkey": "Antoniadis:2012ui",
            "urls": {
                "http://arxiv.org/abs/1210.8336",
                "http://dx.doi.org/10.1007/JHEP04(2012)130",
                "http://inspirehep.net/record/944406",
            },
        },
        {
            "texkey": "2013PhRvD..87a3008P",
            "urls": {
                "http://arxiv.org/abs/1211.2114",
                "http://dx.doi.org/10.1103/PhysRevD.87.013008",
                "http://inspirehep.net/record/1201959",
            },
        },
        {
            "texkey": "Dudas:2012ti",
            "urls": {
                "http://arxiv.org/abs/1211.5609",
                "http://dx.doi.org/10.1016/j.nuclphysb.2013.02.001",
                "http://inspirehep.net/record/1203858",
            },
        },
        {
            "texkey": "Dudas:2013tc",
            "urls": {
                "http://arxiv.org/abs/1309.1179",
                "http://inspirehep.net/record/1252848",
            },
        },
        {
            "texkey": "ATLAScollaboration:2015uw",
            "urls": {
                "http://arxiv.org/abs/1504.05511",
                "http://dx.doi.org/10.1103/PhysRevD.92.032004",
                "http://inspirehep.net/record/1362490",
            },
        },
        {
            "texkey": "CMSCollaboration:2014ke",
            "urls": {
                "http://arxiv.org/abs/1405.3447",
                "http://dx.doi.org/10.1007/JHEP08(2014)174",
                "http://inspirehep.net/record/1296080",
            },
        },
        {
            "texkey": "ATLAScollaboration:2015ue",
            "urls": {
                "http://arxiv.org/abs/1507.05525",
                "http://inspirehep.net/record/1383884",
            },
        },
        {
            "texkey": "ATLAScollaboration:2014ur",
            "urls": {
                "http://arxiv.org/abs/1407.8150",
                "http://dx.doi.org/10.1016/j.physletb.2014.10.002",
                "http://inspirehep.net/record/1308923",
            },
        },
    ]

    assert two_col_keys == expected


def test_extract_texkeys_and_urls_from_pdf_no_crash_on_incomplete_dest_coordinates(pdf_files):
    expected = []
    result = extract_texkeys_and_urls_from_pdf(pdf_files[2])

    assert result == expected


def test_extract_texkeys_from_pdf_no_crash_on_pydpf2_error(pdf_files):
    expected = []
    result = extract_texkeys_and_urls_from_pdf(pdf_files[3])

    assert result == expected


def test_extract_texkeys_from_pdf_no_crash_on_other_exceptions(pdf_files):
    expected = []
    result = extract_texkeys_and_urls_from_pdf(pdf_files[5])

    assert result == expected
