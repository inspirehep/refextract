# -*- coding: utf-8 -*-
#
# This file is part of refextract
# Copyright (C) 2013, 2015, 2016, 2017, 2018 CERN.
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

"""Small library for extracting references used in scholarly communication."""

from __future__ import absolute_import, division, print_function

import os

from setuptools import setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

requirements = [
    'six>=1.7.2',
    'requests>=2.8.1',
    'unidecode>=0.4.18',
    'python-magic>=0.4.12',
    'PyPDF2>=1.26.0',
]

test_requirements = [
    'flake8~=3.0,>=3.5.0',
    'flake8-future-import~=0.0,>=0.4.4',
    'pytest-cov~=2.0,>=2.5.1',
    'pytest>=2.7.0',
    'responses>=0.5.0',
]

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('refextract', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='refextract',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='bibliographic references extraction text-mining',
    license='GPLv2',
    author='CERN',
    author_email='admin@inspirehep.net',
    url='https://github.com/inspirehep/refextract',
    packages=[
        'refextract',
    ],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=requirements,
    extras_require={
        'docs': [
            'Sphinx>=1.3',
            'sphinx_rtd_theme>=0.1.7'
        ],
        'tests': test_requirements
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    tests_require=test_requirements,
)
