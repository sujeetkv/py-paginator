# -*- coding: utf-8 -*-
"""paginator module tests"""
from py_paginator import Paginator


def test_paginator():
    total_items = len(list(range(1, 491)))
    p = Paginator(total_items, item_limit=20)

    p.curr_page = 1
    assert not p.has_prev
    assert p.has_next
    assert p.total_items == 490
    assert p.total_pages == 25
    assert p.next_page == 2
    assert p.get_pager() == {
        'first': 1,
        'prev': None,
        'curr': 1,
        'next': 2,
        'last': 25,
    }
