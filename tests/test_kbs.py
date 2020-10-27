# -*- coding: utf-8 -*-
#
# This file is part of refextract
# Copyright (C) 2020 CERN.
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

from refextract.references.kbs import get_kbs


def test_get_kbs_doesnt_override_default_if_value_is_none():
    cache = get_kbs(custom_kbs={"journals": None})
    assert len(cache["journals"]) == 3
    assert "JHEP" in cache["journals"][-1]


def test_get_kbs_caches_journal_dict():
    journals = {"Journal of Testing": "J.Testing"}

    first_cache = get_kbs(custom_kbs={"journals": journals}).copy()
    assert len(first_cache["journals"]) == 3
    assert ["JOURNAL OF TESTING", "J TESTING"] == first_cache["journals"][-1]

    journals = journals.copy()
    second_cache = get_kbs(custom_kbs={"journals": journals})
    # the cache is reused, so identity of the cache elements doesn't change
    assert all(
        cached_first is cached_second for (cached_first, cached_second)
        in zip(first_cache["journals"], second_cache["journals"])
    )


def test_get_kbs_invalidates_cache_if_input_changes():
    journals = {"Journal of Testing": "J.Testing"}
    first_cache = get_kbs(custom_kbs={"journals": journals}).copy()

    journals = journals = {"Journal of Testing": "J.Test."}
    second_cache = get_kbs(custom_kbs={"journals": journals})
    # the cache is invalidated, so identity of the cache elements changes
    assert all(
        cached_first is not cached_second for (cached_first, cached_second)
        in zip(first_cache["journals"], second_cache["journals"])
    )
    assert len(second_cache["journals"]) == 3
    assert ["JOURNAL OF TESTING", "J TEST"] == second_cache["journals"][-1]
