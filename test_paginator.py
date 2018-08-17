# -*- coding: utf-8 -*-
"""paginator module tests"""
import pytest
from py_paginator import Paginator


@pytest.fixture
def total_items():
    return 490


@pytest.fixture
def item_limit():
    return 20


def test_object(total_items, item_limit):
    assert Paginator(total_items, item_limit)


def test_start_page(total_items, item_limit):
    p = Paginator(total_items, item_limit)

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
    assert p.get_pages() == [
        ('prev', None),
        ('curr', 1),
        ('page', 2),
        ('page', 3),
        ('page', 4),
        ('page', 5),
        ('ellip', '...'),
        ('page', 24),
        ('page', 25),
        ('next', 2),
    ]


def test_middle_page(total_items, item_limit):
    p = Paginator(total_items, item_limit)

    p.curr_page = 10
    assert p.curr_page == 10
    assert p.next_page == 11
    assert p.has_prev
    assert p.get_pager() == {
        'first': 1,
        'prev': 9,
        'curr': 10,
        'next': 11,
        'last': 25,
    }
    assert p.get_pages() == [
        ('prev', 9),
        ('page', 1),
        ('page', 2),
        ('ellip', '...'),
        ('page', 9),
        ('curr', 10),
        ('page', 11),
        ('ellip', '...'),
        ('page', 24),
        ('page', 25),
        ('next', 11),
    ]
