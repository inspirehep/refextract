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

import re
from datetime import datetime

# Sep
re_sep = r"\s*[,\s:-]\s*"
# Sep or no sep
re_sep_opt = r"\s*[,\s:-]?\s*"

# Pattern for PoS journal

# e.g. 2006
re_pos_year_num = r"(?:19|20)\d{2}"
re_pos_year = (
    r"(?P<year>("
    + r"\s"
    + re_pos_year_num
    + r"\s"
    + r"|"
    + r"\("
    + re_pos_year_num
    + r"\)"
    + r"))"
)
# e.g. LAT2007
re_pos_volume = (
    r"(?P<volume_name>\w{1,10})" + re_sep_opt + r"(?P<volume_num>(?:19|20)\d{2})"
)
# e.g. (LAT2007)
re_pos_volume_par = r"\(" + re_pos_volume + r"\)"
# e.g. 20
re_pos_page = r"(?P<page>\d{1,4})"
re_pos_title = r"POS"

re_pos_patterns = [
    re_pos_title
    + re_sep_opt
    + re_pos_year
    + re_sep
    + re_pos_volume
    + re_sep
    + re_pos_page,
    re_pos_title
    + re_sep
    + re_pos_volume
    + re_sep_opt
    + re_pos_year
    + re_sep_opt
    + re_pos_page,
    re_pos_title
    + re_sep
    + re_pos_volume
    + re_sep
    + re_pos_page
    + re_sep_opt
    + re_pos_year,
    re_pos_title + re_sep_opt + re_pos_volume_par + re_sep_opt + re_pos_page,
]
re_opts = re.VERBOSE | re.UNICODE | re.IGNORECASE


def compute_pos_patterns(patterns):
    return [re.compile(p, re_opts) for p in patterns]


re_pos = compute_pos_patterns(re_pos_patterns)

# Pattern for arxiv numbers
# arxiv 9910-1234v9 [physics.ins-det]
re_arxiv = re.compile(
    r"""
    ARXIV[\s:-]*(?P<year>\d{2})-?(?P<month>\d{2})
    [\s.-]*(?P<num>\d{4})(?!\d)(?:[\s-]*V(?P<version>\d))?
    \s*(?P<suffix>\[[A-Z.-]+\])? """,
    re.VERBOSE | re.UNICODE | re.IGNORECASE,
)

re_arxiv_5digits = re.compile(
    r"""
    ARXIV[\s:-]*(?P<year>(1[3-9]|[2-8][0-9]))-?(?P<month>(0[1-9]|1[0-2]))
    [\s.-]*(?P<num>\d{5})(?!\d)(?:[\s-]*V(?P<version>\d))?
    \s*(?P<suffix>\[[A-Z.-]+\])? """,
    re.VERBOSE | re.UNICODE | re.IGNORECASE,
)

# Pattern for arxiv numbers catchup
# arxiv:9910-123 [physics.ins-det]
RE_ARXIV_CATCHUP = re.compile(
    r"""
    ARXIV[\s:-]*(?P<year>\d{2})-?(?P<month>\d{2})
    [\s.-]*(?P<num>\d{3})
    \s*\[(?P<suffix>[A-Z.-]+)\]""",
    re.VERBOSE | re.UNICODE | re.IGNORECASE,
)

# Patterns for ATLAS CONF report numbers
RE_ATLAS_CONF_PRE_2010 = re.compile(
    r"(?<!\w:)ATL(AS)?-CONF-(?P<code>(?:200\d|99)-\d{3})(?![\w\d])"
)
RE_ATLAS_CONF_POST_2010 = re.compile(
    r"(?<!\w:)ATL(AS)?-CONF-(?P<code>20[1-9]\d-\d{3})(?![\w\d])"
)


# Pattern for old arxiv numbers
old_arxiv_numbers = (
    r"[\|/:\s-]?(?P<num>(?:9[1-9]|0[0-7])(?:0[1-9]|1[0-2])\d{3})("
    r"?:v\d{1,3})?(?=[^\w\d]|$)"
)

old_arxiv = {
    r"acc-ph": None,
    r"astro-ph": None,
    r"astro-phy": "astro-ph",
    r"astro-ph\.[a-z]{2}": None,
    r"atom-ph": None,
    r"chao-dyn": None,
    r"chem-ph": None,
    r"cond-mat": None,
    r"cs": None,
    r"cs\.[a-z]{2}": None,
    r"gr-qc": None,
    r"hep-ex": None,
    r"hep-lat": None,
    r"hep-ph": None,
    r"hepph": "hep-ph",
    r"hep-th": None,
    r"hepth": "hep-th",
    r"math": None,
    r"math\.[a-z]{2}": None,
    r"math-ph": None,
    r"nlin": None,
    r"nlin\.[a-z]{2}": None,
    r"nucl-ex": None,
    r"nucl-th": None,
    r"physics": None,
    r"physics\.acc-ph": None,
    r"physics\.ao-ph": None,
    r"physics\.atm-clus": None,
    r"physics\.atom-ph": None,
    r"physics\.bio-ph": None,
    r"physics\.chem-ph": None,
    r"physics\.class-ph": None,
    r"physics\.comp-ph": None,
    r"physics\.data-an": None,
    r"physics\.ed-ph": None,
    r"physics\.flu-dyn": None,
    r"physics\.gen-ph": None,
    r"physics\.geo-ph": None,
    r"physics\.hist-ph": None,
    r"physics\.ins-det": None,
    r"physics\.med-ph": None,
    r"physics\.optics": None,
    r"physics\.plasm-ph": None,
    r"physics\.pop-ph": None,
    r"physics\.soc-ph": None,
    r"physics\.space-ph": None,
    r"plasm-ph": "physics.plasm-ph",
    r"q-bio\.[a-z]{2}": None,
    r"q-fin\.[a-z]{2}": None,
    r"q-alg": None,
    r"quant-ph": None,
    r"quant-phys": "quant-ph",
    r"solv-int": None,
    r"stat\.[a-z]{2}": None,
    r"stat-mech": None,
    r"dg-ga": None,
    r"hap-ph": "hep-ph",
    r"funct-an": None,
    r"quantph": "quant-ph",
    r"stro-ph": "astro-ph",
    r"hepex": "hep-ex",
    r"math-ag": "math.ag",
    r"math-dg": "math.dg",
    r"nuc-th": "nucl-th",
    r"math-ca": "math.ca",
    r"nlin-si": "nlin.si",
    r"quantum-ph": "quant-ph",
    r"ep-ph": "hep-ph",
    r"ep-th": "hep-ph",
    r"ep-ex": "hep-ex",
    r"hept-h": "hep-th",
    r"hepp-h": "hep-ph",
    r"physi-cs": "physics",
    r"asstro-ph": "astro-ph",
    r"hep-lt": "hep-lat",
    r"he-ph": "hep-ph",
    r"het-ph": "hep-ph",
    r"mat-ph": "math.th",
    r"math-th": "math.th",
    r"ucl-th": "nucl-th",
    r"nnucl-th": "nucl-th",
    r"nuclt-th": "nucl-th",
    r"atro-ph": "astro-ph",
    r"qnant-ph": "quant-ph",
    r"astr-ph": "astro-ph",
    r"math-qa": "math.qa",
    r"tro-ph": "astro-ph",
    r"hucl-th": "nucl-th",
    r"math-gt": "math.gt",
    r"math-nt": "math.nt",
    r"math-ct": "math.ct",
    r"math-oa": "math.oa",
    r"math-sg": "math.sg",
    r"math-ap": "math.ap",
    r"quan-ph": "quant-ph",
    r"nlin-cd": "nlin.cd",
    r"math-sp": "math.sp",
    r"ast-ph": "astro-ph",
    r"asyro-ph": "astro-ph",
    r"aastro-ph": "astro-ph",
    r"astrop-ph": "astro-ph",
    r"arxivastrop-ph": "astro-ph",
    r"hept-th": "hep-th",
    r"quan-th": "quant-th",
    r"asro-ph": "astro-ph",
    r"castro-ph": "astro-ph",
    r"asaastro-ph": "astro-ph",
    r"hhep-ph": "hep-ph",
    r"hhep-ex": "hep-ex",
    r"alg-geom": None,
    r"nuclth": "nucl-th",
}


def compute_arxiv_re(report_pattern, report_number):
    if report_number is None:
        report_number = r"\g<name>"
    report_re = re.compile(
        r"(?<!<cds\.REPORTNUMBER>)(?<!\w)"
        + "(?P<name>"
        + report_pattern
        + ")"
        + old_arxiv_numbers,
        re.U | re.I,
    )
    return report_re, report_number


RE_OLD_ARXIV = [compute_arxiv_re(*i) for i in old_arxiv.items()]


def compute_years(start_year=1991):
    current_year = datetime.now().year
    return "|".join(str(y)[2:] for y in range(start_year, current_year + 1))


arxiv_years = compute_years()
arxiv_years_5digits = compute_years(2013)


def compute_months():
    return "|".join(str(y).zfill(2) for y in range(1, 13))


arxiv_months = compute_months()

re_new_arxiv = re.compile(
    r""" # 9910.1234v9 [physics.ins-det]
    (?<!ARXIV:)(?<!\d)
    (?P<year>%(arxiv_years)s)
    (?P<month>(0[1-9]|1[0-2]))
    \.(?P<num>\d{4})(?:[\s-]*V(?P<version>\d))?(?!\d)
    \s*(?P<suffix>\[[A-Z.-]+\])? """
    % {"arxiv_years": arxiv_years},
    re.VERBOSE | re.UNICODE | re.IGNORECASE,
)

re_new_arxiv_5digits = re.compile(
    r""" # 9910.1234v9 [physics.ins-det]
    (?<!ARXIV:)(?<!\d)
    (?P<year>%(arxiv_years)s)
    (?P<month>(0[1-9]|1[0-2]))
    \.(?P<num>\d{5})(?:[\s-]*V(?P<version>\d))?(?!\d)
    \s*(?P<suffix>\[[A-Z.-]+\])? """
    % {"arxiv_years": arxiv_years_5digits},
    re.VERBOSE | re.UNICODE | re.IGNORECASE,
)

# Pattern to recognize quoted text:
re_quoted = re.compile(r'"(?P<title>[^"]+)"', re.UNICODE)

# Pattern to recognise an ISBN for a book:
re_isbn = re.compile(
    r"""
    (?:ISBN[-– ]*(?:|10|13)|International Standard Book Number)
    [:\s]*
    (?P<code>[-\-–0-9Xx]{10,25})""",
    re.VERBOSE | re.UNICODE,
)

# Pattern to recognise a correct knowledge base line:
re_kb_line = re.compile(
    r"^\s*(?P<seek>[^\s].*)\s*---\s*(?P<repl>[^\s].*)\s*$", re.UNICODE
)

# Pattern to recognise references in PDF named destinations
re_reference_in_dest = re.compile(r"^cite\.(.*)$", re.UNICODE)

# precompile some often-used regexp for speed reasons:
re_regexp_character_class = re.compile(r"\[[^\]]+\]", re.UNICODE)
re_multiple_hyphens = re.compile(r"-{2,}", re.UNICODE)


# In certain papers, " bf " appears just before the volume of a
# cited item. It is believed that this is a mistyped TeX command for
# making the volume "bold" in the paper.
# The line may look something like this after numeration has been recognised:
# M. Bauer, B. Stech, M. Wirbel, Z. Phys. bf C : <cds.VOL>34</cds.VOL>
# <cds.YR>(1987)</cds.YR> <cds.PG>103</cds.PG>
# The " bf " stops the title from being correctly linked with its series
# and/or numeration and thus breaks the citation.
# The pattern below is used to identify this situation and remove the
# " bf" component:
re_identify_bf_before_vol = re.compile(r" bf ((\w )?: \<cds\.VOL\>)", re.UNICODE)

# Patterns used for creating institutional preprint report-number
# recognition patterns (used by function "institute_num_pattern_to_regex"):
# Replace "hello" with hello:
re_extract_quoted_text = (
    re.compile(r'\"([^"]+)\"', re.UNICODE),
    r"\g<1>",
)
# Replace / [abcd ]/ with /( [abcd])?/ :
re_extract_char_class = (re.compile(r" \[([^\]]+) \]", re.UNICODE), r"( [\g<1>])?")


# URL recognition:
raw_url_pattern = r"""
        (https?|s?ftp)://(?:[\w\d_.-])+(?::\d{1,5})?
        (?:/[\w\d_.?=&%~∼-]+)*/?
"""
# Stand-alone URL (e.g. http://invenio-software.org/ )
re_raw_url = re.compile(
    "['\"]?(?P<url>" + raw_url_pattern + ")['\"]?", re.UNICODE | re.I | re.VERBOSE
)

# HTML marked-up URL (e.g. <a href="http://invenio-software.org/">
# CERN Document Server Software Consortium</a> )
re_html_tagged_url = re.compile(
    r"""
    # Opening a tag
    <a\s+
    # href attribute
    href\s*=\s*[\'"]
    # href value
    (?P<url>"""
    + raw_url_pattern
    + r""")
    # href closing quote
    ['"]\s*>
    # Tag content
    (?P<desc>[^\<]+)
    # Closing a tag
    </a>""",
    re.UNICODE | re.I | re.VERBOSE,
)


# Numeration recognition pattern - used to identify numeration
# associated with a title when marking the title up into MARC XML:
vol_tag = r"<cds\.VOL\>(?P<vol>[^<]+)<\/cds\.VOL>"
year_tag = r"\<cds\.YR\>\((?P<yr>[^<]+)\)\<\/cds\.YR\>"
series_tag = r"(?P<series>(?:[A-H]|I{1,3}V?|VI{0,3}))?"
page_tag = r"\<cds\.PG\>(?P<pg>[^<]+)\<\/cds\.PG\>"
re_recognised_numeration_title_plus_series = re.compile(
    r"^\s*[\.,]?\s*(?:Ser\.\s*)?"
    + series_tag
    + r"\s*:?\s*"
    + vol_tag
    + r"\s*(?: "
    + year_tag
    + r")?\s*(?: "
    + page_tag
    + r")",
    re.UNICODE,
)

# Another numeration pattern. This one is designed to match marked-up
# numeration that is essentially an IBID, but without the word "IBID". E.g.:
# <cds.JOURNAL>J. Phys. A</cds.JOURNAL> : <cds.VOL>31</cds.VOL>
# <cds.YR>(1998)</cds.YR> <cds.PG>2391</cds.PG>; : <cds.VOL>32</cds.VOL>
# <cds.YR>(1999)</cds.YR> <cds.PG>6119</cds.PG>.
re_numeration_no_ibid_txt = re.compile(
    r"""
          ^((\s*;\s*|\s+and\s+)(?P<series>(?:[A-H]|I{1,3}V?|VI{0,3}))?\s*:?\s
          ## Leading ; : or " and :", and a possible series letter
          \<cds\.VOL\>(?P<vol>\d+|(?:\d+\-\d+))\<\/cds\.VOL>\s                 ## Volume
          \<cds\.YR\>\((?P<yr>[12]\d{3})\)\<\/cds\.YR\>\s                      ## year
          \<cds\.PG\>(?P<pg>[RL]?\d+[c]?)\<\/cds\.PG\>)                        ## page
          """,
    re.UNICODE | re.VERBOSE,
)

re_title_followed_by_series_markup_tags = re.compile(
    r"(\<cds.JOURNAL(?P<ibid>ibid)?\>([^\<]+)\<\/cds.JOURNAL(?:ibid)?\>\s*"
    r".?\s*\<cds\.SER\>([A-H]|(I{1,3}V?|VI{0,3}))\<\/cds\.SER\>)",
    re.UNICODE,
)

re_title_followed_by_implied_series = re.compile(
    r"(\<cds.JOURNAL(?P<ibid>ibid)?\>([^\<]+)\<\/cds.JOURNAL(?:ibid)?\>"
    r"\s*.?\s*([A-H]|(I{1,3}V?|VI{0,3}))\s+:)",
    re.UNICODE,
)


re_punctuation = re.compile(r"[\.\,\;\'\(\)\-]", re.UNICODE)

# The following pattern is used to recognise "citation items" that have been
# identified in the line, when building a MARC XML representation of the line:
re_tagged_citation = re.compile(
    r"""
          \<cds\.                ## open tag: <cds.
          ((?:JOURNAL(?P<ibid>ibid)?)  ## a JOURNAL tag
          |VOL                   ## or a VOL tag
          |YR                    ## or a YR tag
          |PG                    ## or a PG tag
          |REPORTNUMBER          ## or a REPORTNUMBER tag
          |ARXIV                 ## or a ARXIV tag
          |SER                   ## or a SER tag
          |URL                   ## or a URL tag
          |DOI                   ## or a DOI tag
          |QUOTED                ## or a QUOTED tag
          |ISBN                  ## or a ISBN tag
          |PUBLISHER             ## or a PUBLISHER tag
          |COLLABORATION         ## or a COLLABORATION tag
          |AUTH(stnd|etal|incl)) ## or an AUTH tag
          (\s\/)?                ## optional /
          \>                     ## closing of tag (>)
          """,
    re.UNICODE | re.VERBOSE,
)


# is there pre-recognised numeration-tagging within a
# few characters of the start if this part of the line?
re_tagged_numeration_near_line_start = re.compile(
    r"^.{0,4}?<CDS (VOL|SER)>", re.UNICODE
)

re_ibid = re.compile(r"(-|\b)?IBID(EM)?\.?", re.UNICODE)

re_series_from_numeration = re.compile(r"^([A-Za-z])\s*[,\s:-]?\s*\d+", re.UNICODE)
re_series_from_numeration_after_volume = re.compile(
    r"^\d+\s*[,\s:-]?\s*([A-Z])", re.UNICODE
)

# Obtain the series character from the standardised title text
# Only used when no series letter is obtained from numeration matching
re_series_from_title = re.compile(
    r"""
    ([^\s].*)
    (?:[\s\.]+(?:(?P<open_bracket>\()\s*[Ss][Ee][Rr]\.)?
            ([A-H]|(I{1,3}V?|VI{0,3}))
    )?
    (?(open_bracket)\s*\))$
    ## Only match the ending bracket if the opening bracket was found""",
    re.UNICODE | re.VERBOSE,
)


re_wash_volume_tag = (
    re.compile(r"<cds\.VOL>(\w) (\d+)</cds\.VOL>"),
    r"<cds.VOL>\g<1>\g<2></cds.VOL>",
)

# Roman Numbers
re_roman_numbers = r"[XxVvIi]+"

# Possible beginnings of numeration
re_start = r"\s*[,\s:-]?\s*"

# Title tag
re_title_tag = r"(?P<title_tag><cds\.JOURNAL>[^<]*<\/cds\.JOURNAL>)"

# Number (within a volume)
re_volume_sub_number = r"[Nn][oO°]\.?\s*\d{1,6}"
re_volume_sub_number_opt = (
    "(?:" + re_sep + "(?P<vol_sub>" + re_volume_sub_number + "))?"
)

# Volume
re_volume_prefix = r"(?:[Vv]o?l?\.?|[Nn][oO°]\.?)"  # Optional Vol./No.
re_volume_suffix = r"(?:\s*\(\d{1,2}(?:-\d)?\))?"
re_volume_num = r"\d+|" + r"(?:(?<!\w)" + re_roman_numbers + r"(?!\w))"
re_volume_id = (
    r"(?P<vol>(?:(?:[A-Za-z]\s*[,\s:-]?\s*)?(?P<vol_num>%(volume_num)s))|("
    r"?:(?P<vol_num_alt>%(volume_num)s)(?:[A-Za-z]))|(?:(?:[A-Za-z]\s?)?("
    r"?P<vol_num_alt2>\d+)\s*\-\s*(?:[A-Za-z]\s?)?\d+))"
) % {"volume_num": re_volume_num}
re_volume_check = r"(?<![\/\d])"
re_volume = (
    r"\b"
    + "(?:"
    + re_volume_prefix
    + r")?\s*"
    + re_volume_check
    + re_volume_id
    + re_volume_suffix
)

# Month
re_short_month = r"""(?:(?:
[Jj]an|[Ff]eb|[Mm]ar|[Aa]pr|[Mm]ay|[Jj]un|
[Jj]ul|[Aa]ug|[Ss]ep|[Oo]ct|[Nn]ov|[Dd]ec
)\.?)"""

re_month = r"""(?:(?:
[Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay|[Jj]une|
[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember|[Dd]ecember
)\.?)"""

# Year
re_year_num = r"(?:19|20)\d{2}"
re_year_text = "(?P<year>[A-Za-z]?" + re_year_num + ")(?:[A-Za-z]?)"
re_year = r"""
    \(?
    (?:%(short_month)s[,\s]\s*)?  # Jul, 1980
    (?:%(month)s[,\s]\s*)?        # July, 1980
    (?<!\d)
    %(year)s
    (?!\d)
    \)?
""" % {
    "year": re_year_text,
    "short_month": re_short_month,
    "month": re_month,
}

# Page
re_page_prefix = r"[pP]?[p]?\.?\s?"  # Starting page num: optional Pp.
re_page_num = r"[RL]?\w?\d+[cC]?"  # pagenum with optional R/L
re_page_sep = r"\s*-\s*"  # optional separator between pagenums
re_jinst_page = r"(?P<jinst_page>[pP]\d{5}\d*)"
re_page = r"(%s|%s)" % (
    re_jinst_page,
    re_page_prefix
    + "(?P<page>"
    + re_page_num
    + ")(?:"
    + re_page_sep
    + "(?P<page_end>"
    + re_page_num
    + "))?",
)


# Series
re_series = r"(?P<series>[A-H])"

# Used for allowing 3(1991) without space
re_look_ahead_parentesis = r"(?=\()"
re_sep_or_parentesis = "(?:" + re_sep + "|" + re_look_ahead_parentesis + ")"

re_look_behind_parentesis = r"(?<=\))"
re_sep_or_after_parentesis = "(?:" + re_sep + "|" + re_look_behind_parentesis + ")"


# After having processed a line for titles, it may be possible to find more
# numeration with the aid of the recognised titles. The following 2 patterns
# are used for this:

re_correct_numeration_2nd_try_ptn1 = re.compile(
    re_year
    + re_sep  # Year
    + re_title_tag  # Recognised, tagged title
    + "(?P<aftertitle>"
    + re_sep
    + re_volume
    + re_sep  # The volume
    + re_page  # The page
    + ")",
    re.UNICODE | re.VERBOSE,
)

re_correct_numeration_2nd_try_ptn2 = re.compile(
    re_year
    + re_sep
    + re_title_tag
    + "(?P<aftertitle>"
    + re_sep
    + re_volume
    + re_sep
    + re_series
    + re_sep
    + re_page
    + ")",
    re.UNICODE | re.VERBOSE,
)

re_correct_numeration_2nd_try_ptn3 = re.compile(
    re_title_tag
    + "(?P<aftertitle>"
    + re_sep  # Recognised, tagged title
    + re_volume
    + re_sep  # The volume
    + re_page  # The page
    + ")",
    re.UNICODE | re.VERBOSE,
)


re_correct_numeration_2nd_try_ptn4 = re.compile(
    re_title_tag
    + "(?P<aftertitle>"
    + re_sep  # Recognised, tagged title
    + re_year
    + r"\s*[.,\s:]\s*"  # Year
    + re_volume
    + re_sep  # The volume
    + re_page  # The page
    + ")",
    re.UNICODE | re.VERBOSE,
)


# precompile some regexps used to search for and standardize
# numeration patterns in a line for the first time:

# Delete the colon and expressions such as Serie, vol, V. inside the pattern
# <serie : volume> E.g. Replace the string """Series A, Vol 4""" with """A 4"""
re_strip_series_and_volume_labels = (
    re.compile(
        r"(Serie\s|\bS\.?\s)?([A-H])\s?[:,]\s?(\b[Vv]o?l?\.?|\b[Nn]o\.?)?\s?(\d+)",
        re.UNICODE,
    ),
    r"\g<2> \g<4>",
)


# This pattern is not compiled, but rather included in
# the other numeration paterns:
re_nucphysb_subtitle = r"(?:[\(\[]\s*(?:[Ff][Ss]|[Pp][Mm])\s*\d{0,4}\s*[\)\]])"
re_nucphysb_subtitle_opt = "(?:" + re_sep + re_nucphysb_subtitle + ")?"


# the 4 main numeration patterns:

# Pattern 1: <vol, page, year>

# <v, p, y>
re_numeration_vol_page_yr = re.compile(
    re_start
    + re_volume
    + re_volume_sub_number_opt
    + re_sep
    + re_page
    + re_sep_or_parentesis
    + re_year,
    re.UNICODE | re.VERBOSE,
)

# <v, [FS], p, y>
re_numeration_vol_nucphys_page_yr = re.compile(
    re_start
    + re_volume
    + re_volume_sub_number_opt
    + re_sep
    + re_nucphysb_subtitle
    + re_sep
    + re_page
    + re_sep_or_parentesis
    + re_year,
    re.UNICODE | re.VERBOSE,
)

# <[FS], v, p, y>
re_numeration_nucphys_vol_page_yr = re.compile(
    re_start
    + re_nucphysb_subtitle
    + re_sep
    + re_volume
    + re_sep
    + re_page
    + re_sep_or_parentesis
    + re_year,
    re.UNICODE | re.VERBOSE,
)

# Pattern 2: <vol, year, page>

# <v, y, p>
re_numeration_vol_yr_page = re.compile(
    re_start
    + re_volume
    + re_sep_or_parentesis
    + re_year
    + re_sep_or_after_parentesis
    + re_page,
    re.UNICODE | re.VERBOSE,
)

# <v, sv, [FS]?, y, p>
re_numeration_vol_subvol_nucphys_yr_page = re.compile(
    re_start
    + re_volume
    + re_volume_sub_number_opt
    + re_nucphysb_subtitle_opt
    + re_sep_or_parentesis
    + re_year
    + re_sep_or_after_parentesis
    + re_page,
    re.UNICODE | re.VERBOSE,
)

# <v, [FS]?, y, sv, p>
re_numeration_vol_nucphys_yr_subvol_page = re.compile(
    re_start
    + re_volume
    + re_nucphysb_subtitle_opt
    + re_sep_or_parentesis
    + re_year
    + re_volume_sub_number_opt
    + re_sep
    + re_page,
    re.UNICODE | re.VERBOSE,
)

# <[FS]?, v, y, p>
re_numeration_nucphys_vol_yr_page = re.compile(
    re_start
    + re_nucphysb_subtitle
    + re_sep
    +
    # The volume (optional "vol"/"no")
    re_volume
    + re_sep_or_parentesis
    + re_year
    + re_sep_or_after_parentesis  # Year
    + re_page,
    re.UNICODE | re.VERBOSE,
)

# Pattern 3: <vol, serie, year, page>

# <v, s, [FS]?, y, p>
# re_numeration_vol_series_nucphys_yr_page = (re.compile(
#   re_volume + re_sep +
#   re_series + re_sep +
#   _sre_non_compiled_pattern_nucphysb_subtitle + re_sep_or_parentesis +
#   re_year + re_sep +
#   re_page, re.UNICODE|re.VERBOSE), r' \g<series> : ' \
#                                       r'<cds.VOL>\g<vol></cds.VOL> ' \
#                                       r'<cds.YR>(\g<year>)</cds.YR> ' \
#                                       r'<cds.PG>\g<page></cds.PG> ')

# <v, [FS]?, s, y, p
re_numeration_vol_nucphys_series_yr_page = re.compile(
    re_start
    + re_volume
    + re_nucphysb_subtitle_opt
    + re_sep
    + re_series
    + re_sep_or_parentesis
    + re_year
    + re_sep_or_after_parentesis
    + re_page,
    re.UNICODE | re.VERBOSE,
)

# Pattern 4: <vol, serie, page, year>
# <v, s, [FS]?, p, y>
re_numeration_vol_series_nucphys_page_yr = re.compile(
    re_start
    + re_volume
    + re_sep
    + re_series
    + re_nucphysb_subtitle_opt
    + re_sep
    + re_page
    + re_sep
    + re_year,
    re.UNICODE | re.VERBOSE,
)

# <v, [FS]?, s, p, y>
re_numeration_vol_nucphys_series_page_yr = re.compile(
    re_start
    + re_volume
    + re_nucphysb_subtitle_opt
    + re_sep
    + re_series
    + re_sep
    + re_page
    + re_sep
    + re_year,
    re.UNICODE | re.VERBOSE,
)

# Pattern 5: <year, vol, page>
re_numeration_yr_vol_page = re.compile(
    re_start + re_year + re_sep_or_after_parentesis + re_volume + re_sep + re_page,
    re.UNICODE | re.VERBOSE,
)


# Pattern used to locate references of a doi inside a citation
# This pattern matches both url (http) and 'doi:' or 'DOI' formats
re_doi = re.compile(
    r"""
    ((\(?[Dd][Oo][Ii](\s)*\)?:?(\s)*)  # 'doi:' or 'doi' or '(doi)'(upper or lower case)
    |(https?://(dx\.)?doi\.org\/))?    # or 'http://(dx.)doi.org/'
    (?P<doi>10\.                       # 10.                       (mandatory for DOI's)
    \d{3,7}                            # [0-9] x 3-7
    (\.\w+)*                           # subdivisions separated by . (optional)
    (/|%2f)                            # / (possibly urlencoded)
    [\w\-_:;\(\)/\.<>]+                # any character
    [\w\-_:;\(\)/<>])                  # any character excluding a full stop
    """,
    re.VERBOSE + re.IGNORECASE,
)

# Pattern used to locate HDL (handle identifiers)
re_hdl = re.compile(
    r"""([hH][dD][lL]:
                          |https?://hdl\.handle\.net/)
                         (?P<hdl_id>\S+/\S+)""",
    re.UNICODE | re.VERBOSE,
)


def _create_regex_pattern_with_optional_spaces(word):
    """Add the regex special characters (\s*) to allow optional spaces between
    the characters in a word.
    @param word: (string) the word to be inserted into a regex pattern.
    @return: string: the regex pattern for that word with optional spaces
     between all of its characters.
    """
    new_word = ""
    for ch in word:
        if ch.isspace():
            new_word += ch
        else:
            new_word += ch + r"\s*"
    return new_word


def get_reference_section_title_patterns():
    """Return a list of compiled regex patterns used to search for the title of
    a reference section in a full-text document.
    @return: (list) of compiled regex patterns.
    """
    patterns = []
    titles = [
        "references",
        "r\u00c9f\u00e9rences",
        "r\u00c9f\u00c9rences",
        "r\xb4ef\xb4erences",
        "bibliography",
        "bibliographie",
        "literaturverzeichnis",
        "citations",
        "refs",
        "publicationsr\u00e9fs",
        "r\u00c9fs",
        "reference",
        "r\u00e9f\u00e9rence",
        "r\u00c9f\u00c9rence",
    ]
    sect_marker = (
        r"^\s*([\[\-\{\(])?\s*"
        r"((\w|\d){1,5}([\.\-\,](\w|\d){1,5})?\s*"
        r"[\.\-\}\)\]]\s*)?"
        r"(?P<title>"
    )
    sect_marker1 = r"^(\d){1,3}\s*(?P<title>"
    line_end = (
        r"(\s*s\s*e\s*c\s*t\s*i\s*o\s*n\s*)?)\.?([\)\}\]])?"
        r"($|\s*[\[\{\(\<]\s*[1a-z]\s*[\}\)\>\]]|\:$)"
    )

    for t in titles:
        t_ptn = re.compile(
            sect_marker + _create_regex_pattern_with_optional_spaces(t) + line_end,
            re.I | re.UNICODE,
        )
        patterns.append(t_ptn)
        # allow e.g.  'N References' to be found where N is an integer
        t_ptn = re.compile(
            sect_marker1 + _create_regex_pattern_with_optional_spaces(t) + line_end,
            re.I | re.UNICODE,
        )
        patterns.append(t_ptn)

    return patterns


def get_reference_line_numeration_marker_patterns(prefix=""):
    """Return a list of compiled regex patterns used to search for the marker
    of a reference line in a full-text document.
    @param prefix: (string) the possible prefix to a reference line
    @return: (list) of compiled regex patterns.
    """
    title = ""
    if isinstance(prefix, str):
        title = prefix
    g_name = "(?P<mark>"
    g_close = ")"
    space = r"\s*"
    patterns = [
        # [1]
        space + title + g_name + r"\[\s*(?P<marknum>\d+)\s*\]" + g_close,
        # [<letters and numbers]
        space
        + title
        + g_name
        + r"\[\s*[a-zA-Z:-]+\+?\s?(\d{1,4}[A-Za-z:-]?)?\s*\]"
        + g_close,
        # {1}
        space + title + g_name + r"\{\s*(?P<marknum>\d+)\s*\}" + g_close,
        # (1)
        space + title + g_name + r"\<\s*(?P<marknum>\d+)\s*\>" + g_close,
        space + title + g_name + r"\(\s*(?P<marknum>\d+)\s*\)" + g_close,
        space + title + g_name + r"(?P<marknum>\d+)\s*\.(?!\d)" + g_close,
        space + title + g_name + r"(?P<marknum>\d+)\s+" + g_close,
        space + title + g_name + r"(?P<marknum>\d+)\s*\]" + g_close,
        # 1]
        space + title + g_name + r"(?P<marknum>\d+)\s*\}" + g_close,
        # 1}
        space + title + g_name + r"(?P<marknum>\d+)\s*\)" + g_close,
        # 1)
        space + title + g_name + r"(?P<marknum>\d+)\s*\>" + g_close,
        # [1.1]
        space + title + g_name + r"\[\s*\d+\.\d+\s*\]" + g_close,
        # [    ]
        space + title + g_name + r"\[\s*\]" + g_close,
        # *
        space + title + g_name + r"\*" + g_close,
    ]
    return [re.compile(p, re.I | re.UNICODE) for p in patterns]


def get_reference_line_marker_pattern(pattern):
    """Return a list of compiled regex patterns used to search for the first
    reference line in a full-text document.
    The line is considered to start with either: [1] or {1}
    The line is considered to start with : 1. or 2. or 3. etc
    The line is considered to start with : 1 or 2 etc (just a number)
    @return: (list) of compiled regex patterns.
    """
    return re.compile("(?P<mark>" + pattern + ")", re.I | re.UNICODE)


re_reference_line_bracket_markers = get_reference_line_marker_pattern(
    r"(?P<left>\[)\s*(?P<marknum>\d+)\s*(?P<right>\])"
)
re_reference_line_curly_bracket_markers = get_reference_line_marker_pattern(
    r"(?P<left>\{)\s*(?P<marknum>\d+)\s*(?P<right>\})"
)
re_reference_line_dot_markers = get_reference_line_marker_pattern(
    r"(?P<left>)\s*(?P<marknum>\d+)\s*(?P<right>\.)"
)
re_reference_line_number_markers = get_reference_line_marker_pattern(
    r"(?P<left>)\s*(?P<marknum>\d+)\s*(?P<right>)"
)


def get_post_reference_section_title_patterns():
    """Return a list of compiled regex patterns used to search for the title
    of the section after the reference section in a full-text document.
    @return: (list) of compiled regex patterns.
    """
    compiled_patterns = []
    thead = r"^\s*([\{\(\<\[]?\s*(\w|\d)\s*[\)\}\>\.\-\]]?\s*)?"
    ttail = r"(\s*\:\s*)?"
    numatn = r"(\d+|\w\b|i{1,3}v?|vi{0,3})[\.\,]{0,2}\b"
    roman_numbers = r"[LVIX]"
    patterns = [
        # Section titles
        thead + _create_regex_pattern_with_optional_spaces("appendix") + ttail,
        thead + _create_regex_pattern_with_optional_spaces("appendices") + ttail,
        thead
        + _create_regex_pattern_with_optional_spaces("acknowledgement")
        + r"s?"
        + ttail,
        thead
        + _create_regex_pattern_with_optional_spaces("acknowledgment")
        + r"s?"
        + ttail,
        thead
        + _create_regex_pattern_with_optional_spaces("table")
        + r"\w?s?\d?"
        + ttail,
        thead + _create_regex_pattern_with_optional_spaces("figure") + r"s?" + ttail,
        thead
        + _create_regex_pattern_with_optional_spaces("list of figure")
        + r"s?"
        + ttail,
        thead + _create_regex_pattern_with_optional_spaces("annex") + r"s?" + ttail,
        thead
        + _create_regex_pattern_with_optional_spaces("discussion")
        + r"s?"
        + ttail,
        thead + _create_regex_pattern_with_optional_spaces("remercie") + r"s?" + ttail,
        thead + _create_regex_pattern_with_optional_spaces("index") + r"s?" + ttail,
        thead + _create_regex_pattern_with_optional_spaces("summary") + r"s?" + ttail,
        # Figure nums
        r"^\s*" + _create_regex_pattern_with_optional_spaces("figure") + numatn,
        r"^\s*" + _create_regex_pattern_with_optional_spaces("fig") + r"\.\s*" + numatn,
        r"^\s*" + _create_regex_pattern_with_optional_spaces("fig") + r"\.?\s*\d\w?\b",
        # Tables
        r"^\s*" + _create_regex_pattern_with_optional_spaces("table") + numatn,
        r"^\s*" + _create_regex_pattern_with_optional_spaces("tab") + r"\.\s*" + numatn,
        r"^\s*" + _create_regex_pattern_with_optional_spaces("tab") + r"\.?\s*\d\w?\b",
        # Other titles formats
        r"^\s*" + roman_numbers + r"\.?\s*[Cc]onclusion[\w\s]*$",
        r"^\s*Appendix\s[A-Z]\s*\:\s*[a-zA-Z]+\s*",
    ]

    for p in patterns:
        compiled_patterns.append(re.compile(p, re.I | re.UNICODE))

    return compiled_patterns


def get_post_reference_section_keyword_patterns():
    """Return a list of compiled regex patterns used to search for various
    keywords that can often be found after, and therefore suggest the end of,
    a reference section in a full-text document.
    @return: (list) of compiled regex patterns.
    """
    compiled_patterns = []
    patterns = [
        "("
        + _create_regex_pattern_with_optional_spaces("prepared")
        + r"|"
        + _create_regex_pattern_with_optional_spaces("created")
        + r").*(AAS\s*)?\sLATEX",
        r"AAS\s+?LATEX\s+?"
        + _create_regex_pattern_with_optional_spaces("macros")
        + "v",
        r"^\s*"
        + _create_regex_pattern_with_optional_spaces(
            "This paper has been produced using"
        ),
        r"^\s*"
        + _create_regex_pattern_with_optional_spaces(
            "This article was processed by the author using Springer-Verlag"
        )
        + " LATEX",
    ]
    for p in patterns:
        compiled_patterns.append(re.compile(p, re.I | re.UNICODE))
    return compiled_patterns


def regex_match_list(line, patterns):
    """Given a list of COMPILED regex patters, perform the "re.match" operation
    on the line for every pattern.
    Break from searching at the first match, returning the match object.
    In the case that no patterns match, the None type will be returned.
    @param line: (unicode string) to be searched in.
    @param patterns: (list) of compiled regex patterns to search  "line"
     with.
    @return: (None or an re.match object), depending upon whether one of
     the patterns matched within line or not.
    """
    m = None
    for ptn in patterns:
        m = ptn.match(line)
        if m is not None:
            break
    return m


# The different forms of arXiv notation
re_arxiv_notation = re.compile(
    r"""
    (arxiv)|(e[\-\s]?print:?\s*arxiv)
    """,
    re.VERBOSE,
)

# et. al. before J. /// means J is a journal

re_num = re.compile(r"(\d+)")


re_year_in_misc_txt = re.compile(r"(?:^|(?<!\d))(?:19|20)\d{2}(?:(?!\d)|$)")


def remove_year(s, year=None):
    year_pattern = re.escape(year) if year else "(?:19|20)\\d{2}"
    s = re.sub(r"\[\s*%s\s*\]" % year_pattern, "", s)
    s = re.sub(r"\(\s*%s\s*\)" % year_pattern, "", s)
    s = re.sub(r"\s*%s\s*" % year_pattern, "", s)
    return s
