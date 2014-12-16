django-jenkins
==============

Plug and play continuous integration with Django and Jenkins

.. image:: https://requires.io/github/kmmbvnr/django-jenkins/requirements.png?branch=master
   :target: https://requires.io/github/kmmbvnr/django-jenkins/requirements/?branch=master

.. image:: https://pypip.in/d/django-jenkins/badge.png
        :target: https://crate.io/packages/django-jenkins

Installation
------------

From PyPI::

    $ pip install django-jenkins

Or by downloading the source and running::

    $ python setup.py install

Latest git version::

    $ pip install -e git+git://github.com/kmmbvnr/django-jenkins.git#egg=django-jenkins
    $ pip install coverage

Installation for Python 3::

    Works out of the box


Usage
-----

Add ``'django_jenkins'`` to your ``INSTALLED_APPS`` list.
Configure Jenkins to run the following command::

    $ ./manage.py jenkins --enable-coverage

This will create reports/ directory with junit xml, Coverage and Pylint
reports.

For more details see the generic tutorial: https://sites.google.com/site/kmmbvnr/home/django-jenkins-tutorial

Settings
--------

- ``PROJECT_APPS``

  If present, it is supposed to be a list/tuple of django apps for Jenkins to run.
  Tests, reports, and coverage are generated only for the apps from this list.

- ``JENKINS_TASKS``

  List of Jenkins reporters executed by ``./manage.py jenkins`` command.

  Default value::

    JENKINS_TASKS = ()

- ``JENKINS_TEST_RUNNER``

  The name of the class to use for starting the test suite for ``jenkins`` command.
  Class should be inherited from
  ``django_jenkins.runner.CITestSuiteRunner``


Reporters
---------

Here is the reporters prebuild with django-jenkins

- ``django_jenkins.tasks.run_pylint``

  Runs Pylint_ over selected Django apps.

  Task-specific settings: ``PYLINT_RCFILE``

.. _Pylint: http://www.logilab.org/project/pylint

- ``django_jenkins.tasks.run_csslint``

  Runs CSS lint tools over `app/static/*/*.css` files.
  Creates CSS Lint compatible report for Jenkins

  You should have the pylint package installed

- ``django_jenkins.tasks.run_scsslint``

  Runs SCSS lint tools over `app/static/*/*.scss` files.
  Creates CSS Lint compatible report for Jenkins

  You should have the scss-lint_ tool installed

.. _scss-lint: https://github.com/causes/scss-lint

- ``django_jenkins.tasks.run_pep8``

  Runs pep8 tool over selected Django apps.
  Creates Pylint compatible report for Jenkins

  You should have pep8_ python package (>=1.3) installed to run this task.

  Task-specific settings: ``PEP8_RCFILE``

.. _pep8: http://pypi.python.org/pypi/pep8

- ``django_jenkins.tasks.run_pyflakes``

  Runs Pyflakes tool over selected Django apps.
  Creates Pylint compatible report for Jenkins.

  You should have Pyflakes_ python package installed to run this task.

.. _Pyflakes: http://pypi.python.org/pypi/pyflakes

- ``django_jenkins.tasks.run_flake8``

  Runs flake8 tool over selected Django apps.
  Creates Pylint compatible report for Jenkins.

  You should have flake8_ python package installed to run this task.

.. _flake8: http://pypi.python.org/pypi/flake8

- ``django_jenkins.tasks.run_sloccount``

  Runs SLOCCount_ tool over selected Django apps.
  Creates sloccount plugin compatible report for Jenkins.

  You should have the SLOCCount program installed to run this task.

.. _SLOCCount: http://www.dwheeler.com/sloccount/


Changelog
---------

0.16.4 2014-12-15
~~~~~~~~~~~~~~~~~

* New scss-lint task
* Added support for pylint plugins
* Include STATICFILES_DIRS to search path for csslint and jshint
* Search pep8 confing in setup.cfg and tox.ini 
* Fix non-ascii tracback problem
* Fix error handlin in case exception happens in fixture loading
* Fix max-complexity option overriding

Contribution guide
~~~~~~~~~~~~~~~~~~

* Set up local jenkins
* Set up django-jenkins::

    npm install jshint
    npm install csslint
    PATH=$PATH:$WORKSPACE/node_modules/.bin
    tox

* Ensure that everythig works
* Modify the code
* Ensure that everythig works again
* Fix pep8/pyflakes errors and minimize pylint's warninigs
* Pull request!

Authors
-------
Created and maintained by Mikhail Podgurskiy <kmmbvnr@gmail.com>

Contributors: https://github.com/kmmbvnr/django-jenkins/graphs/contributors

Special thanks, for all github forks authors for project extensions ideas and problem identifications.
