# -*- coding: utf-8 -*-
#
# This file is part of refextract
# Copyright (C) 2015, 2016 CERN.
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

# Use Python-2.7:
FROM python:2.7

# Install some prerequisites ahead of `setup.py` in order to profit
# from the docker build cache:
RUN pip install coveralls \
                ipython \
                pep257 \
                pytest \
                pytest-cache \
                pytest-cov \
                pytest-pep8 \
                six \
                sphinx_rtd_theme

# Add sources to `code` and work there:
WORKDIR /code
ADD . /code

# Install refextract:
RUN pip install -e .[docs]

# Run container as user `refextract` with UID `1000`, which should match
# current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' refextract && \
    chown -R refextract:refextract /code

# Run test suite instead of starting the application:
USER refextract
CMD ["python", "setup.py", "test"]
