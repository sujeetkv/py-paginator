# -*- coding: utf-8 -*-
"""paginator module to generate page numbers for pagination"""

import math


__all__ = ['Paginator']


class Paginator(object):
    """Paginator class to generate page numbers for pagination.

    :param total_items: number of total items

    :param item_limit: number of items per page

    :param curr_page: current page number
    """
    def __init__(self, total_items, item_limit, curr_page=1):
        self.total_items = int(total_items)
        self._item_limit = int(item_limit)
        self._curr_page = int(curr_page)
        self.first_page = 1
        self._process_page_numbers()


    @property
    def curr_page(self):
        """Current page number."""
        return self._curr_page


    @curr_page.setter
    def curr_page(self, curr_page):
        self._curr_page = curr_page
        self._process_page_numbers()


    @property
    def item_limit(self):
        """Number of items per page."""
        return self._item_limit


    @item_limit.setter
    def item_limit(self, item_limit):
        self._item_limit = item_limit
        self._process_page_numbers()


    @property
    def total_pages(self):
        """Number of total pages."""
        return self.last_page


    @property
    def has_pages(self):
        """Check if has multiple pages."""
        return (self.last_page > self.first_page)


    @property
    def has_prev(self):
        """Check if has previous page."""
        return (self._curr_page > self.first_page)


    @property
    def has_next(self):
        """Check if has next page."""
        return (self._curr_page < self.last_page)


    def get_pager(self):
        """Get pager dict.

        Returns a dict having current and edged page numbers.
        """
        pager = {}
        if self.has_pages:
            pager['first'] = self.first_page
            pager['prev'] = self.prev_page if self.has_prev else None
            pager['curr'] = self._curr_page
            pager['next'] = self.next_page if self.has_next else None
            pager['last'] = self.last_page
        return pager


    def get_pages(self, adjacents=1):
        """Get page numbers list.

        :param adjacents: number of adjacent page numbers of current page in compact state
        """
        self.page_list = []

        adjacents = int(adjacents) if adjacents else 1
        adj_count = adjacents * 2

        if self.has_pages:
            second_last = self.last_page - 1

            # prev
            if self.has_prev:
                self.page_list.append(('prev', self.prev_page))
            else:
                self.page_list.append(('prev', None))

            if self.last_page < (7 + adj_count):# not enough pages to hide anything
                self._append_range_pages(1, self.last_page + 1)
            elif self.last_page >= (5 + adj_count):# enough pages to hide some
                # close to beggining; only hide later pages
                if self._curr_page < (1 + adj_count):
                    self._append_range_pages(1, 4 + adj_count)
                    self.page_list.append(('ellip', '...'))
                    self.page_list.append(('page', second_last))
                    self.page_list.append(('page', self.last_page))
                # in middle; hide some front and some back
                elif (self.last_page - adj_count) > self._curr_page and self._curr_page > adj_count:
                    self.page_list.append(('page', 1))
                    self.page_list.append(('page', 2))
                    self.page_list.append(('ellip', '...'))
                    self._append_range_pages(self._curr_page - adjacents, self._curr_page + adjacents + 1)
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
            if self.has_next:
                self.page_list.append(('next', self.next_page))
            else:
                self.page_list.append(('next', None))

        return self.page_list


    def _process_page_numbers(self):
        self.last_page = int(math.ceil(float(self.total_items) / float(self.item_limit)))
        if self._curr_page < 1 or self._curr_page > self.last_page:
           self._curr_page = 1
        self.prev_page = self._curr_page - 1
        self.next_page = self._curr_page + 1
        self.item_offset = self.prev_page * self.item_limit
        self.page_list = []


    def _append_range_pages(self, start, stop):
        for counter in range(start, stop):
            if counter == self._curr_page:
                self.page_list.append(('curr', counter))
            else:
                self.page_list.append(('page', counter))
