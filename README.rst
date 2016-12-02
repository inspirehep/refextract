..
   This file is part of refextract
   Copyright (C) 2015, 2016 CERN.

   refextract is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation; either version 2 of the
   License, or (at your option) any later version.

   refextract is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with refextract; if not, write to the Free Software Foundation, Inc.,
   59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

   In applying this license, CERN does not waive the privileges and immunities
   granted to it by virtue of its status as an Intergovernmental Organization
   or submit itself to any jurisdiction.


============
refextract
============


Small library for extracting references used in scholarly communication.

* Free software: GPLv2
* Documentation: http://pythonhosted.org/refextract/
* Issues and pull requests: https://github.com/inspirehep/refextract

*Originally exported from Invenio https://github.com/inveniosoftware/invenio.*


Dependencies
============
* [file](http://linux.die.net/man/1/file)
* [pdftotext](http://linux.die.net/man/1/pdftotext)

Installation
============

.. code-block:: shell

    pip install refextract

Usage
=====

To get structured info from a publication reference:

.. code-block:: python

    from refextract import extract_journal_reference
    reference = extract_journal_reference("J.Phys.,A39,13445")
    print(reference)
    {
        'extra_ibids': [],
        'is_ibid': False,
        'misc_txt': u'',
        'page': u'13445',
        'title': u'J. Phys.',
        'type': 'JOURNAL',
        'volume': u'A39',
        'year': ''
     }


To extract references from a publication full-text PDF:

.. code-block:: python

    from refextract import extract_references_from_file
    reference = extract_references_from_file("some/fulltext/1503.07589v1.pdf")
    print(reference)
    [
            {'author': [u'F. Englert and R. Brout'],
             'doi': [u'10.1103/PhysRevLett.13.321'],
             'journal_page': [u'321'],
             'journal_reference': ['Phys.Rev.Lett.,13,1964'],
             'journal_title': [u'Phys.Rev.Lett.'],
             'journal_volume': [u'13'],
             'journal_year': [u'1964'],
             'linemarker': [u'1'],
             'title': [u'Broken symmetry and the mass of gauge vector mesons'],
             'year': [u'1964']}, ...
    ]

You can also extract directly from a URL:

.. code-block:: python

    from refextract import extract_references_from_url
    reference = extract_references_from_url("http://arxiv.org/pdf/1503.07589v1.pdf")
    print(reference)
    [
             {'author': [u'F. Englert and R. Brout'],
              'doi': [u'10.1103/PhysRevLett.13.321'],
              'journal_page': [u'321'],
              'journal_reference': ['Phys.Rev.Lett.,13,1964'],
              'journal_title': [u'Phys.Rev.Lett.'],
              'journal_volume': [u'13'],
              'journal_year': [u'1964'],
              'linemarker': [u'1'],
              'title': [u'Broken symmetry and the mass of gauge vector mesons'],
              'year': [u'1964']}, ...
    ]
