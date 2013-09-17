#!/usr/bin/env python
import os
import re
from setuptools import setup, find_packages

__doc__="""
Reusable blog application for Django
"""

version = '1.0.1'

setup(name='django-fusionbox-blog',
    version=version,
    description=__doc__,
    author='Fusionbox programmers',
    author_email='programmers@fusionbox.com',
    keywords='django blog',
    long_description=__doc__,
    url='https://github.com/fusionbox/django-fusionbox-blog',
    packages=find_packages(),
    namespace_packages=['fusionbox'],
    platforms = "any",
    license='BSD',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
    install_requires = ['django_fusionbox'],
    requires = ['django_fusionbox'],
)
