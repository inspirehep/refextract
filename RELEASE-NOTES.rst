==============================
 refextract v0.2.1 is released
==============================

refextract v0.2.1 was released on 2017-07-02.

About
-----

Small library for extracting references used in scholarly communication.

What's new
----------

- Named destinations may not always have left and top coordinates. This case is
  now handled gracefully: no TeXkeys are returned by ``extract_texkeys_from_pdf``
  instead of raising an uncaught exception.

- Makes ``CFG_PATH_GFILE`` and ``CFG_PATH_PDFTOTEXT`` configurable through shell
  variables, with fallback on the output of ``which``, in order to allow for
  easier containerization.

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
