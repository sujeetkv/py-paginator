# -*- coding: utf-8 -*-
"""paginator module to generate page numbers for pagination"""
import math

__title__ = 'py_paginator'
__version__ = '0.0.1'
__author__ = 'Sujeet Kumar'
__email__ = 'sujeetkv90@gmail.com'
__uri__ = 'https://github.com/sujeet-kumar/py-paginator'
__description__ = 'Paginator to generate page numbers for pagination'
__doc__ = 'Paginator to generate page numbers for pagination'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2018 Sujeet Kumar <sujeetkv90@gmail.com>'
__status__ = 'Development'

__all__ = ['Paginator']


class Paginator(object):
    """Paginator class generate page numbers for pagination

    :param total_items: number of total items
    :param item_limit: number of items per page
    :param curr_page: current page number
    """
    def __init__(self, total_items, item_limit, curr_page):
        self.total_items = int(total_items)
        self.item_limit = int(item_limit)
        self.curr_page = int(curr_page)
        self.first_page = 1
        self.last_page = int(math.ceil(float(self.total_items) / float(self.item_limit)))
        if self.curr_page < 1 or self.curr_page > self.last_page:
           self.curr_page = 1
        self.prev_page = self.curr_page - 1
        self.next_page = self.curr_page + 1
        self.item_offset = self.prev_page * self.item_limit
        self.page_list = []


    @property
    def has_pages(self):
        """Check if has multiple pages"""
        return (self.last_page > 1)


    def get_pager(self):
        """Get pager dict

        Get dict having edged page numbers
        """
        pager = {}
        if self.has_pages:
            pager['curr_page'] = self.curr_page
            pager['last_page'] = self.last_page
            if self.curr_page > 1:
                pager['first'] = self.first_page
                pager['prev'] = self.prev_page
            else:
                pager['first'] = None
                pager['prev'] = None
            pager['curr'] = self.curr_page
            if self.curr_page < self.last_page:
                pager['next'] = self.next_page
                pager['last'] = self.last_page
            else:
                pager['next'] = None
                pager['last'] = None
        return pager


    def get_pages(self, adjacents=1):
        """Get page numbers list

        :param adjacents: number of adjacent page numbers of current page in compact state
        """
        self.page_list = []

        adjacents = int(adjacents) if adjacents else 1
        adj_count = adjacents * 2

        if self.has_pages:
            second_last = self.last_page - 1

            # prev
            if self.curr_page > self.first_page:
                self.page_list.append(('prev', self.prev_page))
            else:
                self.page_list.append(('prev', None))

            if self.last_page < (7 + adj_count):# not enough pages to hide anything
                self._append_range_pages(1, self.last_page + 1)
            elif self.last_page >= (5 + adj_count):# enough pages to hide some
                # close to beggining; only hide later pages
                if self.curr_page < (1 + adj_count):
                    self._append_range_pages(1, 4 + adj_count)
                    self.page_list.append(('ellip', '...'))
                    self.page_list.append(('page', second_last))
                    self.page_list.append(('page', self.last_page))
                # in middle; hide some front and some back
                elif (self.last_page - adj_count) > self.curr_page and self.curr_page > adj_count:
                    self.page_list.append(('page', 1))
                    self.page_list.append(('page', 2))
                    self.page_list.append(('ellip', '...'))
                    self._append_range_pages(self.curr_page - adjacents, self.curr_page + adjacents + 1)
                    self.page_list.append(('ellip', '...'))
                    self.page_list.append(('page', second_last))
                    self.page_list.append(('page', self.last_page))
                # close to end; only hide early pages
                else:
                    self.page_list.append(('page', 1))
                    self.page_list.append(('page', 2))
                    self.page_list.append(('ellip', '...'))
                    self._append_range_pages(self.last_page - (1 + (adjacents * 3)), self.last_page + 1)

            # next
            if self.curr_page < self.last_page:
                self.page_list.append(('next', self.next_page))
            else:
                self.page_list.append(('next', None))

        return self.page_list


    def _append_range_pages(self, start, stop):
        for counter in range(start, stop):
            if counter == self.curr_page:
                self.page_list.append(('curr', counter))
            else:
                self.page_list.append(('page', counter))