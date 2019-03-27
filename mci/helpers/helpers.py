"""General Purpose Helper Functions."""

import math
from collections import OrderedDict


def compute_offset(page, items_per_page):
    """Compute the offset value for pagination.

    Args:
        page (int): The current page to compute the offset from.
        items_per_page (int): Number of items per page.

    Returns:
        int: The offset value.

    """
    return (page - 1) * items_per_page


def compute_page(offset, items_per_page):
    """Compute the current page number based on offset.

    Args:
        offset (int): The offset to use to compute the page.
        items_per_page (int): Nimber of items per page.

    Returns:
        int: The page number.

    """

    return int(math.ceil((offset / items_per_page))) + 1


def build_links(endpoint: str, offset: int, limit: int, rows: int):
    """Build links for a paginated response

    Args:
        endpoint (str): Name of the endpoint to provide in the link.
        offset (int): Database query offset.
        limit (int): Number of items to return in query.
        rows (int): Count of rows in table.

    Returns:
        dict: The links based on the offset and limit

    """

    # URL and pages
    url_link = '/{}?offset={}&limit={}'
    total_pages = int(math.ceil(rows / limit))
    current_page = compute_page(offset, limit)

    # Links
    links = OrderedDict()
    current = OrderedDict()
    first = OrderedDict()
    prev = OrderedDict()
    next = OrderedDict()
    last = OrderedDict()

    links = []

    current['rel'] = 'self'
    current['href'] = url_link.format(endpoint, offset, limit)
    links.append(current)

    first['rel'] = 'first'
    first['href'] = url_link.format(endpoint, compute_offset(1, limit))
    links.append(first)

    if current_page > 1:
        prev['rel'] = 'prev'
        prev['href'] = url_link.format(
            endpoint, compute_offset(current_page - 1, limit), limit)
        links.append(prev)

    if current_page < total_pages:
        next['rel'] = 'next'
        next['href'] = url_link.format(
            endpoint, compute_offset(current_page + 1, limit), limit)
        links.append(next)

    last['rel'] = 'last'
    last['href'] = url_link.format(
        endpoint, compute_offset(total_pages, limit), limit)
    links.append(last)

    return links
