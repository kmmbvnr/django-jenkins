#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from os import path
from setuptools import setup


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

install_requires=[
    'Django>=1.8',
]

# Needed for Python <2.7
try:
    import importlib
    import unittest
except ImportError:
    install_requires.append(['importlib', 'unittest'])

setup(
    name='django-jenkins',
    version='0.16.4',
    author='Mikhail Podgurskiy',
    author_email='kmmbvnr@gmail.com',
    description='Plug and play continuous integration with django and jenkins',
    long_description=read(path.abspath(path.join(path.dirname(__file__), 'README.rst'))),
    license='LGPL',
    platforms=['Any'],
    keywords=['pyunit', 'unittest', 'testrunner', 'hudson', 'jenkins',
              'django', 'pylint', 'pep8', 'pyflakes', 'csslint', 'scsslint',
              'jshint', 'coverage'],
    url='http://github.com/kmmbvnr/django-jenkins',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
    ],
    install_requires=install_requires,
    packages=['django_jenkins', 'django_jenkins.management',
              'django_jenkins.tasks', 'django_jenkins.management.commands'],
    package_data={'django_jenkins': ['tasks/pylint.rc']},
    zip_safe=False,
    include_package_data=True
)
