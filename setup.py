#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'django-hudson',
    version = '0.9.0',
    author = 'Mikhail Podgurskiy',
    author_email = 'kmmbvnr@gmail.com',
    description = 'Plug and play continuous integration with django and hudson',
    license = 'LGPL',
    platforms = ['Any'],
    keywords = ['pyunit', 'unittest', 'testrunner', 'hudson', 'django'],
    url = 'http://github.com/kmmbvnr/django-hudson',
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
        'Django>=1.2',
        'coverage>=3.4b1',
        'pylint',
    ],
    packages = ['django_hudson', 'django_hudson.management', 'django_hudson.management.commands'],
    package_data={'django_hudson': ['management/commands/pylint.rc']},
    zip_safe = False,
    include_package_data = True
)
