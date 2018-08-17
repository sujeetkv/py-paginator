# -*- coding: utf-8 -*-
"""paginator module setup"""
from setuptools import setup
import py_paginator


setup(
    name=py_paginator.__title__,
    version=py_paginator.__version__,
    license=py_paginator.__license__,
    author=py_paginator.__author__,
    author_email=py_paginator.__email__,
    description=py_paginator.__description__,
    long_description=py_paginator.__doc__,
    url=py_paginator.__uri__,
    py_modules=['py_paginator'],
    include_package_data=True,
    platforms='any',
    keywords='paginator py_paginator py-paginator',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
