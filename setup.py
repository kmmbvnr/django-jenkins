#!/usr/bin/env python
import codecs
from os import path
from subprocess import check_call
from distutils.core import setup
from distutils.command.build import build

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


class build_with_submodules(build):
    def run(self):
        if path.exists('.git'):
            check_call(['git', 'submodule', 'init'])
            check_call(['git', 'submodule', 'update'])
        build.run(self)

setup(
    name = 'django-jenkins',
    cmdclass={"build": build_with_submodules},
    version = '0.12.1',
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
    requires=[
        'Django (>=1.3)',
        'coverage (>=3.4)',
        'pylint (>=0.23)',
    ],
    packages = ['django_jenkins', 'django_jenkins.management', 'django_jenkins.tasks', 'django_jenkins.management.commands'],
    package_data={'django_jenkins': ['tasks/pylint.rc', 'tasks/jslint_runner.js', 'tasks/jslint/jslint.js', 'tasks/csslint/release/csslint-rhino.js']},
)
