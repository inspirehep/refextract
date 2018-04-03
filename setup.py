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

from setuptools import find_packages, setup


url = 'https://github.com/inspirehep/refextract'

readme = open('README.rst').read()

setup_requires = [
    'autosemver~=0.0,>=0.5.3',
]

install_requires = [
    'PyPDF2~=1.0,>=1.26.0',
    'autosemver~=0.0,>=0.5.3',
    'python-magic~=0.0,>=0.4.15',
    'requests~=2.0,>=2.18.4',
    'six~=1.0,>=1.10.0',
    'unidecode~=1.0,>=1.0.22',
]

docs_require = [
    'Sphinx~=1.0,>=1.7.1',
]

tests_require = [
    'flake8-future-import~=0.0,>=0.4.4',
    'flake8~=3.0,>=3.5.0',
    'pytest-cov~=2.0,>=2.5.1',
    'pytest~=3.0,>=3.4.2',
    'responses~=0.0,>=0.8.1',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
    'tests:python_version=="2.7"': [
        'unicode-string-literal~=1.0,>=1.1',
    ],
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name not in ['all', 'tests:python_version=="2.7"']:
        extras_require['all'].extend(reqs)

packages = find_packages(exclude=['docs'])

setup(
    name='refextract',
    autosemver={
        'bugtracker_url': url + '/issues',
    },
    url=url,
    license='GPLv2',
    author='CERN',
    author_email='admin@inspirehep.net',
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    description=__doc__,
    long_description=readme,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
