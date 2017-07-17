..
   This file is part of refextract
   Copyright (C) 2015, 2016, 2017 CERN.

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


Changes
=======

Version 0.2.2 (2017-07-17)

- Handle pyPDF2 internal errors.

Version 0.2.1 (2017-07-02)

- Named destinations may not always have left and top coordinates. This case is
  now handled gracefully: no TeXkeys are returned by ``extract_texkeys_from_pdf``
  instead of raising an uncaught exception.

- Makes ``CFG_PATH_GFILE`` and ``CFG_PATH_PDFTOTEXT`` configurable through
  shell variables, with fallback on the output of ``which``, in order to allow
  for easier containerization.

Version 0.2.0 (2017-06-26)

- Substantial rewrite of the API. In particular:

  * ``extract_references_from_file``, ``extract_references_from_string``, and
    ``extract_references_from_url`` now return a list of the references,
    instead of an object with keys ``stats`` and ``references``.

  * If the number of TeXkeys that were extracted from the PDF metadata matches
    the number of references parsed by RefExtract, an extra ``texkey`` field is
    added to each returned reference.

  * The API now raises exceptions when it encounters an unrecoverable error.

  * Finally, the API now returns the list of raw references on which
    ``refextract`` worked.

Version 0.1.0 (2016-01-12)

- Initial export from Invenio Software <https://github.com/inveniosoftware/invenio>
- Restructured into stripped down, standalone version
