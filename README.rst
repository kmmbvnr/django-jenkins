django-jenkins
==============

Plug and play continuous integration with Django and Jenkins

Installation
------------

From PyPI::

    $ pip install django-jenkins

Or by downloading the source and running::

    $ python setup.py install

For the latest git version, you need the latest pip installed first::

    $ pip install git+https://github.com/pypa/pip.git
    $ pip install -e git+git://github.com/kmmbvnr/django-jenkins.git#egg=django-jenkins

.. _PyPI: http://pypi.python.org/

Usage
-----

Add ``'django_jenkins'`` to your ``INSTALLED_APPS`` list.
Configure Jenkins to run the following command::

    $ ./manage.py jenkins

This will create reports/ directory with junit xml, Coverage and Pylint
reports.

For more details see the generic tutorial: https://sites.google.com/site/kmmbvnr/home/django-jenkins-tutorial
or tutorial for running django-jenkins on ShiningPanda CI https://docs.shiningpanda.com/tutorials/multi-databases/project.html

Settings
--------

- ``PROJECT_APPS``

  if presents, it is supposed to be a list/tuple of django apps for Jenkins to run.
  Tests, reports and coverage are generated only for the apps from this list.
  You should specify --all option to ignore this settings.

- ``JENKINS_TASKS``

  List of Jenkins tasks executed by ``./manage.py jenkins`` command.

  Default value::

    JENKINS_TASKS = (
        'django_jenkins.tasks.run_pylint',
        'django_jenkins.tasks.with_coverage',
        'django_jenkins.tasks.django_tests',
    )

- ``JENKINS_TEST_RUNNER``

  The name of the class to use for starting the test suite for ``jenkins``
  and ``jtest`` commands. Class should be inherited from
  ``django_jenkins.runner.CITestSuiteRunner``

Tasks
-----

Here is the list of tasks prebuild with django-jenkins

- ``django_jenkins.tasks.run_pylint``

  Runs Pylint_ over selected Django apps.

.. _Pylint: http://www.logilab.org/project/pylint

- ``django_jenkins.tasks.with_coverage``

  Produces XML coverage report for Jenkins

- ``django_jenkins.tasks.django_tests``

  Discovers standard Django test suite from test.py files

- ``django_jenkins.tasks.dir_tests``

  Discover tests from all test*.py files in app subdirectories

- ``django_jenkins.tasks.run_jslint``

  Runs jslint tools over ``<app>/static/*/*.js`` files.
  Creates Pylint compatible report for Jenkins

  You should have the rhino_ or nodejs_ javascript interpreter installed for jslint

- ``django_jenkins.tasks.run_csslint``

  Runs CSS lint tools over `app/static/*/*.css` files.
  Creates CSS Lint compatible report for Jenkins

  You should have the rhino_ or nodejs_ javascript interpreter installed for csslint

.. _rhino: http://www.mozilla.org/rhino/
.. _nodejs: http://nodejs.org/

- ``django_jenkins.tasks.run_pep8``

  Runs pep8 tool over selected Django apps.
  Creates Pylint compatible report for Jenkins

  You should have pep8_ python package (>=1.3) installed to run this task

.. _pep8: http://pypi.python.org/pypi/pep8

- ``django_jenkins.tasks.run_pyflakes``

  Runs Pyflakes tool over selected Django apps.
  Creates Pylint compatible report for Jenkins.

  You should have Pyflakes_ python package installed to run this task

.. _Pyflakes: http://pypi.python.org/pypi/pyflakes

- ``django_jenkins.tasks.run_sloccount``

  Runs SLOCCount_ tool over selected Django apps.
  Creates sloccount plugin compatible report for Jenkins.

  You should have the SLOCCount program installed to run this task

.. _SLOCCount: http://www.dwheeler.com/sloccount/

- ``django_jenkins.tasks.lettuce_tests``

  Discover Lettuce tests from app/feature directories.

  You should have the Lettuce_ Python package installed to run this task

.. _Lettuce: http://lettuce.it/

- ``django_jenkins.tasks.with_local_celery``

  Replacement for ``djcelery.tests.runners.CeleryTestSuiteRunner``
  Change settings for run Celery_ tasks locally.

.. _Celery: http://ask.github.com/django-celery/

Changelog
---------

0.13.0 2012-07-15
~~~~~~~~~~~~~~~~~
* unittest2 compatibility
* **WARNING:** Junit test data now stored in one junit.xml file
* Support for pep8 1.3
* New in-directory test discovery task
* Added --liveserver option
* Fixes in jslint and csslint tasks

0.12.1 2012-03-15
~~~~~~~~~~~~~~~~~
* Added Celery task
* Add nodejs support for jslint and csslint tasks
* Improve js and css files selection
* Bug fixes

0.12.0 2012-01-15
~~~~~~~~~~~~~~~~~

* Django 1.3 in requirements
* Windmill support was removed (Django 1.4 has a better implementation)
* Ignore South migrations by default
* Added SLOCCount task
* Added Lettuce testing task
* Added CSS Lint task
* Used xml output format for jslint
* Used native pep8 output format

0.11.1 2010-06-15
~~~~~~~~~~~~~~~~~

* Do not produce file reports for jtest command by default
* Ignore Django apps without models.py file, as in Django test command
* Fix jslint_runner.js packaging
* Fix coverage file filtering

0.11.0 2010-04-15
~~~~~~~~~~~~~~~~~

* Support pep8, Pyflakes, jslint tools
* Added jtest command
* Allow specify custom test runner
* Various fixes, thnk githubbers :)

0.10.0 2010-02-15
~~~~~~~~~~~~~~~~~

* Pluggable ci tasks refactoring
* Alpha support for windmill tests
* Partial python 2.4 compatibility
* Renamed to django-jenkins

0.9.1 2010-12-15
~~~~~~~~~~~~~~~~

* Python 2.5 compatibility
* Make compatible with latest Pylint only

0.9.0 2010-10-15
~~~~~~~~~~~~~~~~

* Initial public release


Authors
-------
Mikhail Podgurskiy <kmmbvnr@gmail.com>

Contributors:

* Chris Heisel (https://github.com/cmheisel)
* Andrey Fedoseev (https://github.com/andreyfedoseev)
* Jannis Leidel (https://github.com/jezdez)
* Luciano Pacheco (https://github.com/lucmult)
* Julien Lirochon (https://github.com/jlirochon)
* Olivier Girardot (https://github.com/ssaboum)
* Victor Safronovich (https://github.com/suvit)
* Bradley Ayers (https://github.com/bradleyayers)
* Jonas Obrist (https://github.com/ojii)
* John Paulett (https://github.com/johnpaulett)
* Michael Ellingen (https://github.com/mvantellingen)
* Domen Kožar (https://github.com/iElectric)
* Simon Panay (https://github.com/simonpanay)
* Tom Mortimer-Jones (https://github.com/morty)
* Philip Kimmey (https://github.com/philipkimmey)
* Peter Baumgartner (https://github.com/ipmb)

Special thanks, for all github forks authors not listed here 
for for project extensions ideas and problem identifications.

