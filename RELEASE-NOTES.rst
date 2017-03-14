==============================
 refextract v0.2.0 is released
==============================

refextract v0.2.0 was released on 2017-06-26.

About
-----

Small library for extracting references used in scholarly communication.

What's new
----------

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

Installation
------------

   $ pip install refextract

Documentation
-------------

   http://pythonhosted.org/refextract/

Homepage
--------

   https://github.com/inspirehep/refextract

Good luck and thanks for choosing refextract!

| INSPIRE Development Team
|   Email: feedback@inspirehep.net
|   Twitter: http://twitter.com/inspirehep
|   GitHub: http://github.com/inspirehep
|   URL: http://inspirehep.net
