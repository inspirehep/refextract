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

import pytest

from refextract.references.engine import (
    get_plaintext_document_body,
    parse_references,
)

from refextract.references.errors import UnknownDocumentTypeError


def get_references(ref_line, override_kbs_files=None):
    return parse_references([ref_line], override_kbs_files=override_kbs_files)


def test_month_with_year():
    ref_line = u"""[2] S. Weinberg, A Model of Leptons, Phys. Rev. Lett. 19 (Nov, 1967) 1264–1266."""
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'S. Weinberg, A Model of Leptons'],
            'journal_page': [u'1264-1266'],
            'journal_reference': [u'Phys. Rev. Lett. 19 (1967) 1264-1266'],
            'journal_title': [u'Phys. Rev. Lett.'],
            'journal_volume': [u'19'],
            'journal_year': [u'1967'],
            'linemarker': [u'2'],
            'year': [u'1967'],
            'raw_ref': [ref_line],
        }
    ]
    assert references == expected


def test_numeration_not_finding_year():
    ref_line = u"""[137] M. Papakyriacou, H. Mayer, C. Pypen, H. P. Jr., and S. Stanzl-Tschegg, “Inﬂuence of loading frequency on high cycle fatigue properties of b.c.c. and h.c.p. metals,” Materials Science and Engineering, vol. A308, pp. 143–152, 2001."""
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'M. Papakyriacou, H. Mayer, C. Pypen, H. P. Jr., and S. Stanzl-Tschegg'],
            'journal_page': [u'143-152'],
            'journal_reference': [u'Mat.Sci.Eng. A308 (2001) 143-152'],
            'journal_title': [u'Mat.Sci.Eng.'],
            'journal_volume': [u'A308'],
            'journal_year': [u'2001'],
            'linemarker': [u'137'],
            'year': [u'2001'],
            'title': [u'Influence of loading frequency on high cycle fatigue properties of b.c.c. and h.c.p. metals'],
            'raw_ref': [ref_line],
        }
    ]
    assert references == expected


def test_numeration_not_finding_year2():
    ref_line = u"""[138] Y.-B. Park, R. Mnig, and C. A. Volkert, “Frequency effect on thermal fatigue damage in Cu interconnects,” Thin Solid Films, vol. 515, pp. 3253– 3258, 2007."""
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'Y.-B. Park, R. Mnig, and C. A. Volkert'],
            'journal_page': [u'3253-3258'],
            'journal_reference': [u'Thin Solid Films 515 (2007) 3253-3258'],
            'journal_title': [u'Thin Solid Films'],
            'journal_volume': [u'515'],
            'journal_year': [u'2007'],
            'linemarker': [u'138'],
            'year': [u'2007'],
            'title': [u'Frequency effect on thermal fatigue damage in Cu interconnects'],
            'raw_ref': [ref_line],
        }
    ]
    assert references == expected


def test_extra_a_in_report_number():
    ref_line = u'[14] CMS Collaboration, CMS-PAS-HIG-12-002. CMS Collaboration, CMS-PAS-HIG-12-008. CMS Collaboration, CMS-PAS-HIG-12-022. ATLAS Collaboration, arXiv:1205.0701. ATLAS Collaboration, ATLAS-CONF-2012-078.'
    res = get_references(ref_line)
    references = res[0]
    assert len(references) == 1
    assert references[0]['collaboration'] == [
        u'CMS Collaboration',
        u'ATLAS Collaboration',
    ]
    assert references[0]['reportnumber'] == [
        u'CMS-PAS-HIG-12-002',
        u'CMS-PAS-HIG-12-008',
        u'CMS-PAS-HIG-12-022',
        u'arXiv:1205.0701',
        u'ATLAS-CONF-2012-078',
    ]
    assert references[0]['linemarker'] == [u'14']


def test_fermi_report_number_AD_APC():
    ref_line = u'[8] V. Lebedev et al. (PIP-II Collaboration), The PIP-II Conceptual Design Report, FERMILAB-TM-2649-AD-APC (2017).'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'FERMILAB-TM-2649-AD-APC']
    assert references[0]['linemarker'] == [u'8']


def test_fermi_report_number_AD_APC_TD():
    ref_line = u'[9] G. Ambrosio et al., Fermilab Report Fermilab-FN-0954-AD-APC-TD (2013).'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'FERMILAB-FN-0954-AD-APC-TD']
    assert references[0]['linemarker'] == [u'9']


def test_fermi_report_number_no_suffix():
    ref_line = u'[8] T.  H.  Nicol,  "TESLA  Test  Cell  Cryostat  Support  Post  Thermal  and Structural Analysis, "FERMILAB-TM-1794, Fermilab, 1992.'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'FERMILAB-TM-1794']
    assert references[0]['linemarker'] == [u'8']


def test_fermi_report_number_mulitple():
    ref_line = u'[17] ILC Collaboration, G. Aaronset al., ILC Reference Design Report Volume 1 - Executive Summary, FERMILAB-DESIGN-2007-03, FERMILAB-PUB-07-794-E, arXiv:0712.1950 [physics.acc-ph].'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [
        u'FERMILAB-Design-2007-03',
        u'FERMILAB-Pub-07-794-E',
        u'arXiv:0712.1950 [physics.acc-ph]'
    ]
    assert references[0]['linemarker'] == [u'17']


def test_fermi_report_number_ESH():
    ref_line = u'[11] T. Sanami, Applicability of a Bonner Sphere technique for pulsed neutron in 120 GeV proton facility, in Proceedings of the 22nd Workshop on Radiation Detectors and Their Uses, pp. 148-159, FERMILAB-CONF-08-203-AD-APC-E-ESH (2008).'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'FERMILAB-Conf-08-203-AD-APC-E-ESH']
    assert references[0]['linemarker'] == [u'11']


def test_fermi_report_number_wdrs():
    ref_line = u'[5] M. Bardeen & M. Wayne, E-Labs - Learning with Authentic Data, FERMILAB-CONF-16-205-WDRS (2016).'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'FERMILAB-Conf-16-205-WDRS']
    assert references[0]['linemarker'] == [u'5']


def test_not_fermi_report_number():
    ref_line = u'[17]  S.-h. Lee, C. DeTar, H. Na, and D. Mohler (Fermilab Lattice, MILC), (2014), arXiv:1411.1389 [hep-lat].'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'arXiv:1411.1389 [hep-lat]']
    assert references[0]['linemarker'] == [u'17']


def test_d0_cdf_note_report_number():
    ref_line = u'[7] CDF and D0 Collaborations, CDF Note 9787, D0 Note 5928 (2009); T. Aaltonenet al. (CDF Collaboration), Phys. Rev. Lett.100, 161802 (2008);'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [
        u'CDF-NOTE-9787',
        u'D0-Note-5928'
    ]
    assert references[0]['linemarker'] == [u'7']


def test_d0_symbol_report_number():
    ref_line = u'[71] J. Estrada, C. Garcia, B. Hoeneisen, and P. Rubinov, "MCM II and the Trip chip," FERMILAB-TM-2226 (DØ note 4009), 2002.'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [
        u'FERMILAB-TM-2226',
        u'D0-Note-4009'
    ]
    assert references[0]['linemarker'] == [u'71']


def test_d0_conf_note_report_number():
    ref_line = u'[4]  D0 Collaboration, D0 Note 6417-CONF (2015)'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'D0-Note-6417-CONF']
    assert references[0]['linemarker'] == [u'4']


def test_fermilab_proposal_report_number():
    ref_line = u'7. A Proposal to Measure νμ → νe Oscillations and νgm Disappearance at the Fermilab Booster: BooNEE. Church, et al. (Eds.), Fermilab Proposal 898 (1997)'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'FERMILAB-Proposal-898']
    assert references[0]['linemarker'] == [u'7']


def test_false_fermilab_proposal_report_number():
    ref_line = u'[10] T. Roberts, et al., 1976, Fermilab proposal neutron - deuteron elastic scattering'
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'T. Roberts, et al.'],
            'linemarker': [u'10'],
            'misc': [u'Fermilab proposal neutron - deuteron elastic scattering'],
            'year':[u'1976'],
            'raw_ref': [ref_line],
        }
    ]
    assert references == expected


def test_microboone_note_report_number():
    ref_line = u'[9] The MicroBooNE Collaboration. Space Charge Effect Measurements and Corrections. MICROBOONE-NOTE-1018-PUB, 2016. URL http://www-microboone.fnal.gov/publications/publicnotes/index.html.'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'MICROBOONE-NOTE-1018-PUB']
    assert references[0]['linemarker'] == [u'9']


def test_microboone_fale_report_numbr():
    ref_line = u'[40] MicroBooNE, LAr1-ND, ICARUS-WA104 collaboration, M. Antonello et al., A Proposal for a Three Detector Short-Baseline Neutrino Oscillation Program in the Fermilab Booster Neutrino Beam, 1503.01520.'
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'M. Antonello et al.'],
            'linemarker': [u'40'],
            'misc': [u'MicroBooNE, LAr1-ND, ICARUS-WA104 collaboration',
                     u'A Proposal',
                     u'for a Three Detector Short-Baseline Neutrino Oscillation Program in the Fermilab Booster Neutrino Beam'],
            'raw_ref': [ref_line],
            'reportnumber': [u'arXiv:1503.01520'],
        }
    ]
    assert references == expected


def test_slac_report_number_5_digits():
    ref_line = u'[25] Proton-nucleus scattering approximations and implications for LHC crystal collimation, Report No. SLAC-PUB14030, https://www.slac.stanford.edu/cgi-wrap/getdoc/slac-pub-14030.pdf. REDUCTION OF 400 GeV=c SLOW EXTRACTION \u2026 PHYS. REV. ACCEL. BEAMS 23, 023501 (2020) 023501-13'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['reportnumber'] == [u'SLAC-PUB-14030']
    assert references[0]['linemarker'] == [u'25']


def test_doi_4_digit():
    ref_line = u'[32]  E. Armengaud, et al., JINST 10(05), P05007 (2015). doi:10.1088/1748-0221/10/05/P05007.'
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'E. Armengaud, et al.'],
            'doi': [u'doi:10.1088/1748-0221/10/05/P05007'],
            'journal_page': [u'P05007'],
            'journal_reference': [u'JINST 10 (2015) P05007'],
            'journal_title': [u'JINST'],
            'journal_volume': [u'10'],
            'journal_year': [u'2015'],
            'linemarker': [u'32'],
            'raw_ref': [ref_line],
            'year': [u'2015'],
        }
    ]
    assert references == expected


def test_doi_5_digit_multi():
    ref_line = u'38 R. Aaij et al. (LHCb Collaboration), "Measurement of charged particle multiplicities in pp collisions at ps = 7 TeV in the forward region", Eur. Phys. J. C (2012) 72: 1947. DOI: 10.1140/epjc/s10052-012-1947-8. HepData DOI: 10.17182/hepdata.65435.'
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'author': [u'R. Aaij et al.'],
            'misc': [u'(LHCb Collaboration)'],
            'title': [u'Measurement of charged particle multiplicities in pp collisions at ps = 7 TeV in the forward region'],
            'doi': [u'doi:10.1140/epjc/s10052-012-1947-8'],
            'journal_page': [u'1947'],
            'journal_reference': [u'Eur. Phys. J. C 72 (2012) 1947'],
            'journal_title': [u'Eur. Phys. J. C'],
            'journal_volume': [u'72'],
            'journal_year': [u'2012'],
            'linemarker': [u'38'],
            'year': [u'2012'],
            'raw_ref': [ref_line],
        },
        {
            'author': [u'R. Aaij et al.'],
            'misc': [u'HepData'],
            'doi': [u'doi:10.17182/hepdata.65435'],
            'linemarker': [u'38'],
            'raw_ref': [ref_line],
        }
    ]
    assert references == expected


def test_doi_subdivisions():
    ref_line = u'[10] A. Smith et al., "Introduction to Particle Physics", 2017, Springer Publishing, ISBN: 97881925212214, DOI: 10.978.819252/12214.'
    res = get_references(ref_line)
    references = res[0]
    assert references[0]['doi'] == [u'doi:10.978.819252/12214']
    assert references[0]['linemarker'] == [u'10']


def test_get_plaintext_document_body(tmpdir):
    input = [u"Some text\n", u"on multiple lines\n"]
    f = tmpdir.join("plain.txt")
    f.write("".join(input))
    assert input == get_plaintext_document_body(str(f))

    with pytest.raises(UnknownDocumentTypeError) as excinfo:
        html = "<html><body>Some page</body></html>"
        f = tmpdir.join("page.html")
        f.write(html)
        get_plaintext_document_body(str(f))
    assert 'text/html' in excinfo.value


def test_reference_split():
    ref_line = "[7] J. Ellis et al., Phys. Lett. B 212, 375 (1988); H. Ejiri et al., Phys. Lett. B 317, 14 (1993)."
    res = get_references(ref_line)
    references = res[0]
    expected = [
        {
            'journal_title': [u'Phys. Lett. B'],
            'author': [u'J. Ellis et al.'],
            'year': [u'1988'],
            'journal_volume': [u'212'],
            'journal_reference': [u'Phys. Lett. B 212 (1988) 375'],
            'journal_year': [u'1988'],
            'linemarker': [u'7'],
            'raw_ref': ['[7] J. Ellis et al., Phys. Lett. B 212, 375 (1988); H. Ejiri et al., Phys. Lett. B 317, 14 (1993).'], 'journal_page': [u'375']
        },
        {
            'author': [u'H. Ejiri et al.'],
            'journal_page': [u'14'],
            'journal_reference': [u'Phys. Lett. B 317 (1993) 14'],
            'journal_title': [u'Phys. Lett. B'],
            'journal_volume': [u'317'],
            'journal_year': [u'1993'],
            'linemarker': [u'7'],
            'raw_ref': ['[7] J. Ellis et al., Phys. Lett. B 212, 375 (1988); H. Ejiri et al., Phys. Lett. B 317, 14 (1993).'],
            'year': [u'1993']
        }
    ]
    assert references == expected


def test_reference_split_ibid():
    ref_line = """[17] See for example: Hagelin J S, Kelley S and Tanaka T 1994 Nucl. Phys. B 415 (1994) 293. Moroi T 1996
Phys. Rev. D 53 6565 [Erratum-ibid. D 56 (1997) 4424] (Preprint hep-ph/9512396)."""
    res = get_references(ref_line)
    references = res[0]
    assert len(references) == 3
    assert references[2]['journal_title'] == [u'Phys. Rev. D']
    assert references[2]['journal_volume'] == [u'D56']
    assert references[2]['journal_page'] == [u'4424']
    assert references[2]['journal_year'] == [u'1997']


def test_reference_split_handles_authors_correctly():
    ref_line = "[27] K. P. Das and R. C. Hwa, Phys. Lett.B 68, (1977) 459; Erratum Phys. Lett.B 73(1978) 504; D. Mol-nar and S. A. Voloshin, Phys. Rev. Lett.91(2003) 092301; V. Greco, C.M. Ko and P. Levai, Phys.Rev.C 68(2003) 034904; B. Zhang, Lie-Wen Chen and C. M. Ko, Phys.Rev.C 72(2005) 024906. R. J. Fries et al.Ann. Rev. Nucl. Part. Sci.58, (2008)177."
    res = get_references(ref_line)
    references = res[0]
    authors = [ref["author"] for ref in references]
    expected = [
        ["K. P. Das and R. C. Hwa"],
        ["K. P. Das and R. C. Hwa"],
        ["D. Mol-nar and S. A. Voloshin"],
        ["V. Greco, C.M. Ko and P. Levai"],
        ["B. Zhang"],
        ["R. J. Fries et al."],
    ]
    assert authors == expected


def test_reference_split_handles_repeated_fields():
    ref_line = u"[20] A. Buchel, \u201cFinite temperature resolution of the Klebanov-Tseytlin singularity,\u201d Nucl. Phys. B 600, 219 (2001) [hep-th/0011146]. A. Buchel, C. P. Herzog, I. R. Klebanov, L. A. Pando Zayas and A. A. Tseytlin, \u201cNonextremal gravity duals for fractional D-3 branes on the conifold,\u201d JHEP 0104 (2001) 033 [hep-th/0102105]."
    res = get_references(ref_line)
    references = res[0]
    assert references == [
        {
            'author': [u'A. Buchel'],
            'journal_page': [u'219'],
            'journal_reference': [u'Nucl. Phys. B 600 (2001) 219'],
            'journal_title': [u'Nucl. Phys. B'],
            'journal_volume': [u'600'],
            'journal_year': [u'2001'],
            'linemarker': [u'20'],
            'raw_ref': [u'[20] A. Buchel, \u201cFinite temperature resolution of the Klebanov-Tseytlin singularity,\u201d Nucl. Phys. B 600, 219 (2001) [hep-th/0011146]. A. Buchel, C. P. Herzog, I. R. Klebanov, L. A. Pando Zayas and A. A. Tseytlin, \u201cNonextremal gravity duals for fractional D-3 branes on the conifold,\u201d JHEP 0104 (2001) 033 [hep-th/0102105].'],
            'reportnumber': [u'hep-th/0011146'],
            'title': [u'Finite temperature resolution of the Klebanov-Tseytlin singularity'],
            'year': [u'2001']
        },
        {
            'author': [u'A. Buchel, C. P. Herzog, I. R. Klebanov, L. A. Pando Zayas and A. A. Tseytlin'],
            'journal_page': [u'033'],
            'journal_reference': [u'J. High Energy Phys. 0104 (2001) 033'],
            'journal_title': [u'J. High Energy Phys.'],
            'journal_volume': [u'0104'],
            'journal_year': [u'2001'],
            'linemarker': [u'20'],
            'raw_ref': [u'[20] A. Buchel, \u201cFinite temperature resolution of the Klebanov-Tseytlin singularity,\u201d Nucl. Phys. B 600, 219 (2001) [hep-th/0011146]. A. Buchel, C. P. Herzog, I. R. Klebanov, L. A. Pando Zayas and A. A. Tseytlin, \u201cNonextremal gravity duals for fractional D-3 branes on the conifold,\u201d JHEP 0104 (2001) 033 [hep-th/0102105].'],
            'reportnumber': [u'hep-th/0102105'],
            'title': [u'Nonextremal gravity duals for fractional D-3 branes on the conifold'],
            'year': [u'2001']
        }
    ]


def test_reference_split_handles_semicolon():
    ref_line = "[7] Y.   Nara,   A.   Ohnishi,   and   H.   Stocker,arXiv:1601.07692 [hep-ph]; V. P. Konchakovski, W.Cassing, Yu. B. Ivanov and V. D. Toneev, Phys.Rev.C 90, 014903 (2014);"
    res = get_references(ref_line)
    references = res[0]
    assert len(references) == 2


def test_clean_pdf_before_run(tmp_path, pdf_files):
    tmp_file_path = tmp_path / "packed.pdf"
    pdf = pdf_files[6]
    with open(pdf, 'rb') as input, open(tmp_file_path.as_posix(), 'wb') as tmp_out:
        tmp_out.write(input.read())

    text = get_plaintext_document_body(tmp_file_path.as_posix())
    assert text == ['Test\n', '\x0c']
