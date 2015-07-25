===================================
 extractutils v0.1.1 is released
===================================

extractutils v0.1.0 was released on 2015-07-22

About
-----

Small library for persistent identifiers used in scholarly communication.

What's new
----------

- Fixes GND validation and normalization.
- Replaces invalid package name in `run-tests.sh` and makes `run-tests.sh` file
  executable. One can now use `docker-compose run --rm web /code/run-tests.sh`
  to run all the CI tests (pep257, sphinx, test suite).
- Initial release of Docker configuration suitable for local developments.
  `docker-compose build` rebuilds the image,
  `docker-compose run --rm web /code/run-tests.sh` runs the test suite.

Installation
------------

   $ pip install extractutils

Documentation
-------------

   http://extractutils.readthedocs.org/en/v0.1.1

Homepage
--------

   https://github.com/inveniosoftware/extractutils

Good luck and thanks for choosing extractutils.

| Invenio Development Team
|   Email: info@invenio-software.org
|   Twitter: http://twitter.com/inveniosoftware
|   GitHub: http://github.com/inveniosoftware
|   URL: http://invenio-software.org
