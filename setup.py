#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'django-jenkins',
    version = '0.10.0',
    author = 'Mikhail Podgurskiy',
    author_email = 'kmmbvnr@gmail.com',
    description = 'Plug and play continuous integration with django and jenkins',
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
        'Django>=1.2',
        'coverage>=3.4',
        'pylint>=0.23',
    ],
    packages = ['django_jenkins', 'django_jenkins.management', 'django_jenkins.tasks', 'django_jenkins.management.commands'],
    package_data={'django_jenkins': ['tasks/pylint.rc']},
    zip_safe = False,
    include_package_data = True
)
