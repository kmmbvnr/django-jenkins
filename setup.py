#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from os import path
from setuptools import setup


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


setup(
    name='django-jenkins',
    version='1.11.0',
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
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
    ],
    install_requires=[
        'Django>=1.8',
    ],
    packages=['django_jenkins', 'django_jenkins.management',
              'django_jenkins.tasks', 'django_jenkins.management.commands'],
    package_data={'django_jenkins': ['tasks/pylint.rc']},
    zip_safe=False,
    include_package_data=True
)
