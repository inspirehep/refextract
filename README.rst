..
   This file is part of refextract
   Copyright (C) 2015, 2016, 2018 CERN.

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

.. image:: https://travis-ci.org/inspirehep/refextract.svg?branch=master
    :target: https://travis-ci.org/inspirehep/refextract

.. image:: https://coveralls.io/repos/github/inspirehep/refextract/badge.svg?branch=master
    :target: https://coveralls.io/github/inspirehep/refextract?branch=master


About
=====

A small library for extracting references used in scholarly communication.


Install
=======

.. code-block:: console

    $ pip install refextract


Usage
=====

To get structured information from a publication reference:

.. code-block:: python

    >>> from refextract import extract_journal_reference
    >>> reference = extract_journal_reference('J.Phys.,A39,13445')
    >>> print(reference)
    {
        'extra_ibids': [],
        'is_ibid': False,
        'misc_txt': u'',
        'page': u'13445',
        'title': u'J. Phys.',
        'type': 'JOURNAL',
        'volume': u'A39',
        'year': '',
    }

To extract references from a PDF:

.. code-block:: python

    >>> from refextract import extract_references_from_file
    >>> references = extract_references_from_file('1503.07589.pdf')
    >>> print(references[0])
    {
        'author': [u'F. Englert and R. Brout'],
        'doi': [u'doi:10.1103/PhysRevLett.13.321'],
        'journal_page': [u'321'],
        'journal_reference': [u'Phys. Rev. Lett. 13 (1964) 321'],
        'journal_title': [u'Phys. Rev. Lett.'],
        'journal_volume': [u'13'],
        'journal_year': [u'1964'],
        'linemarker': [u'1'],
        'raw_ref': [u'[1] F. Englert and R. Brout, \u201cBroken symmetry and the mass of gauge vector mesons\u201d, Phys. Rev. Lett. 13 (1964) 321, doi:10.1103/PhysRevLett.13.321.'],
        'texkey': [u'Englert:1964et'],
        'year': [u'1964'],
    }

To extract directly from a URL:

.. code-block:: python

    >>> from refextract import extract_references_from_url
    >>> references = extract_references_from_url('https://arxiv.org/pdf/1503.07589.pdf')
    >>> print(references[0])
    {
        'author': [u'F. Englert and R. Brout'],
        'doi': [u'doi:10.1103/PhysRevLett.13.321'],
        'journal_page': [u'321'],
        'journal_reference': [u'Phys. Rev. Lett. 13 (1964) 321'],
        'journal_title': [u'Phys. Rev. Lett.'],
        'journal_volume': [u'13'],
        'journal_year': [u'1964'],
        'linemarker': [u'1'],
        'raw_ref': [u'[1] F. Englert and R. Brout, \u201cBroken symmetry and the mass of gauge vector mesons\u201d, Phys. Rev. Lett. 13 (1964) 321, doi:10.1103/PhysRevLett.13.321.'],
        'texkey': [u'Englert:1964et'],
        'year': [u'1964'],
    }


Notes
=====

``refextract`` depends on `pdftotext`_.

.. _`pdftotext`: http://linux.die.net/man/1/pdftotext


Acknowledgments
===============

``refextract`` is based on code and ideas from the following people, who
contributed to the ``docextract`` module in Invenio:

- Alessio Deiana
- Federico Poli
- Gerrit Rindermann
- Graham R. Armstrong
- Grzegorz Szpura
- Jan Aage Lavik
- Javier Martin Montull
- Micha Moskovic
- Samuele Kaplun
- Thorsten Schwander
- Tibor Simko


License
=======

GPLv2
