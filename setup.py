#!/usr/bin/env python
import codecs
from os import path
from setuptools import setup

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

setup(
    name = 'django-jenkins',
    version = '0.12.0',
    author = 'Mikhail Podgurskiy',
    author_email = 'kmmbvnr@gmail.com',
    description = 'Plug and play continuous integration with django and jenkins',
    long_description=read(path.abspath(path.join(path.dirname(__file__), 'README.rst'))),
    license = 'LGPL',
    platforms = ['Any'],
    keywords = ['pyunit', 'unittest', 'testrunner', 'hudson', 'jenkins', 'django'],
    url = 'http://github.com/kmmbvnr/django-jenkins',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
    ],
    install_requires=[
        'Django>=1.3',
        'coverage>=3.4',
        'pylint>=0.23',
    ],
    packages = ['django_jenkins', 'django_jenkins.management', 'django_jenkins.tasks', 'django_jenkins.management.commands'],
    package_data={'django_jenkins': ['tasks/pylint.rc', 'tasks/jslint_runner.js', 'tasks/jslint/jslint.js', 'tasks/csslint/release/csslint-rhino.js']},
    zip_safe = False,
    include_package_data = True
)
