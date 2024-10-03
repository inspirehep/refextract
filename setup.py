# -*- coding: utf-8 -*-
#
# This file is part of refextract
# Copyright (C) 2013, 2015, 2016, 2017, 2018, 2020 CERN.
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

from setuptools import find_packages, setup

url = 'https://github.com/inspirehep/refextract'

with open('README.rst') as file:
    readme = file.read()

install_requires = [
    'PyPDF2~=1.0,>=1.26.0',
    'python-magic~=0.0,>=0.4.15',
    'requests~=2.0,>=2.18.4',
    'six~=1.0,>=1.10.0',
    'unidecode~=1.0,>=1.0.22',
    'inspire-utils~=3.0,>=3.0.25',
    'Flask>=2.0.3',
    "webargs<=5.4.0",
    "gunicorn>=20.1.0",
    "prometheus-flask-exporter~=0.20,>=0.20.1"
]

tests_require = [
    'flake8-future-import~=0.0,>=0.4.4',
    'flake8~=3.0,>=3.5.0',
    'pytest-cov~=2.0,>=2.10',
    'pytest~=4.0,>=4.6',
    'responses~=0.0,>=0.8.1',
    'mock>=4.0.3'
]

extras_require = {
    'tests': tests_require,
}

extras_require['all'] = []
for _name, reqs in extras_require.items():
    extras_require['all'].extend(reqs)

packages = find_packages()

setup(
    name='refextract',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
