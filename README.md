# py-paginator
Paginator to generate page numbers for pagination


## Usage Example

```python
from py_paginator import Paginator

total_records = 400 # records count from database
page = 1 # page number from url

paginator = Paginator(total_items=total_records, item_limit=20, curr_page=page)
```

use this `paginator` object in templates to create pagination links

`paginator.item_limit` and `paginator.item_offset` can be used in database query to apply limit


## Sample jinja macro for flask framework

```html
{#: PAGINATION ------------------------------------------------------ #}
{#
    :paginator: paginator object
    :endpoint: flask request endpoint
    :only_pager: If True it will show a pager instead of numbered pagination
#}
{% macro pagination(paginator, endpoint=None, only_pager=False) %}
    {% if not endpoint %}
        {% set endpoint = request.endpoint %}
    {% endif %}
    {% if 'page' in kwargs %}
        {% set _ = kwargs.pop('page') %}
    {% endif %}
    {% if paginator.has_pages %}
    <nav aria-label="Page navigation">
        {% if only_pager %}
            {% set pager = paginator.get_pager() %}
            <ul class="pager">
                <li class="previous{% if not paginator.has_prev %} disabled{% endif %}">
                    <a href="{% if paginator.has_prev %}{{ pager.prev }}{% else %}#{% endif %}"><span aria-hidden="true">&laquo;</span> Prev</a>
                </li>
                <li class="next{% if not paginator.has_next %} disabled{% endif %}">
                    <a href="{% if paginator.has_next %}{{ pager.next }}{% else %}#{% endif %}">Next <span aria-hidden="true">&raquo;</span></a>
                </li>
            </ul>
        {% else %}
            <ul class="pagination">
                {% for page_type, page_num in paginator.get_pages() %}
                    {% if page_type == 'prev' %}
                        {% if page_num %}
                            <li><a href="{{ url_for(endpoint, page=page_num, **kwargs) }}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>
                        {% else %}
                            <li class="disabled"><span><span aria-hidden="true">&laquo;</span></span></li>
                        {% endif %}
                    {% elif page_type == 'next' %}
                        {% if page_num %}
                            <li><a href="{{ url_for(endpoint, page=page_num, **kwargs) }}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>
                        {% else %}
                            <li class="disabled"><span><span aria-hidden="true">&raquo;</span></span></li>
                        {% endif %}
                    {% elif page_type == 'ellip' %}
                        <li class="disabled"><span><span aria-hidden="true">&hellip;</span></span></li>
                    {% elif page_type == 'curr' %}
                        <li class="active"><span>{{ page_num }}</span></li>
                    {% else %}
                        <li><a href="{{ url_for(endpoint, page=page_num, **kwargs) }}">{{ page_num }}</a></li>
                    {% endif %}
                {% endfor %}
            </ul>
        {% endif %}
    </nav>
    {% endif %}
{% endmacro %}
```
