# py-paginator
Paginator to generate page numbers for pagination

[![Build Status](https://travis-ci.org/sujeetkv/py-paginator.svg?branch=master)](https://travis-ci.org/sujeetkv/py-paginator)
[![PyPI Version](https://img.shields.io/pypi/v/py-paginator.svg)](https://pypi.org/project/py-paginator)

## Installation

```bash
pip install py-paginator
```

## Usage Example with flask framework

- **app.py**

```python
from flask import Flask, request, render_template
from py_paginator import Paginator

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')

@app.route('/')
def home():
    page = int(request.args.get('page', 1))
    limit = 20

    records_count = get_records_count() # get records count from storage

    paginator = Paginator(total_items=records_count, item_limit=limit, curr_page=page)

    records = get_records(limit=paginator.item_limit, offset=paginator.item_offset) # get records from storage

    return render_template('home.html', records=records, paginator=paginator)
```

 Here `paginator.item_limit` and `paginator.item_offset` can be used in database query to apply limit. `paginator` object can be used in templates to create pagination links.

- **templates/macros.html**

```html
{#
    :paginator: Paginator object
    :endpoint: flask request endpoint
    :pager: If True it will show a pager instead of numbered pagination

    - you can also pass further arguments that will be passed into `url_for()` of every link.
#}
{% macro render_pagination(paginator, endpoint=request.endpoint, pager=False) %}
    {% if paginator.has_pages %}
        {% do kwargs.update(request.args) %}
        {% do kwargs.pop('page', None) %}
        <nav aria-label="Page navigation">
            {% if pager %}
                {% set pager = paginator.get_pager() %}
                <ul class="pager">
                    <li class="previous{% if not paginator.has_prev %} disabled{% endif %}">
                        {% do kwargs.update({'page': pager.prev}) %}
                        <a href="{% if paginator.has_prev %}{{ url_for(endpoint, **kwargs) }}{% else %}#{% endif %}"><span aria-hidden="true">&laquo;</span> Prev</a>
                    </li>
                    <li class="next{% if not paginator.has_next %} disabled{% endif %}">
                        {% do kwargs.update({'page': pager.next}) %}
                        <a href="{% if paginator.has_next %}{{ url_for(endpoint, **kwargs) }}{% else %}#{% endif %}">Next <span aria-hidden="true">&raquo;</span></a>
                    </li>
                </ul>
            {% else %}
                <ul class="pagination">
                    {% for page_type, page_num in paginator.get_pages() %}
                        {% do kwargs.update({'page': page_num}) %}
                        {% if page_type == 'prev' %}
                            {% if page_num %}
                                <li><a href="{{ url_for(endpoint, **kwargs) }}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>
                            {% else %}
                                <li class="disabled"><span><span aria-hidden="true">&laquo;</span></span></li>
                            {% endif %}
                        {% elif page_type == 'next' %}
                            {% if page_num %}
                                <li><a href="{{ url_for(endpoint, **kwargs) }}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>
                            {% else %}
                                <li class="disabled"><span><span aria-hidden="true">&raquo;</span></span></li>
                            {% endif %}
                        {% elif page_type == 'ellip' %}
                            <li class="disabled"><span><span aria-hidden="true">&hellip;</span></span></li>
                        {% elif page_type == 'curr' %}
                            <li class="active"><span>{{ page_num }}</span></li>
                        {% else %}
                            <li><a href="{{ url_for(endpoint, **kwargs) }}">{{ page_num }}</a></li>
                        {% endif %}
                    {% endfor %}
                </ul>
            {% endif %}
        </nav>
    {% endif %}
{% endmacro %}
```

- **templates/home.html**

```html
{% from "macros.html" import render_pagination with context %}

<h1>Total Records: {{ paginator.total_items }}</h1>
<h2>Total Pages: {{ paginator.total_pages }}</h2>

{% for record in records %}
    <p>{{ loop.index + paginator.item_offset }} - {{ record.field_name }}</p>
{% else %}
    <p>No Records found.</p>
{% endfor %}

{{ render_pagination(paginator) }}
```
