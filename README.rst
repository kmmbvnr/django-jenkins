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

Installation for Python 3::

    Works out of the box


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

  If present, it is supposed to be a list/tuple of django apps for Jenkins to run.
  Tests, reports, and coverage are generated only for the apps from this list.
  You should specify --all option to ignore this setting.

- ``JENKINS_TASKS``

  List of Jenkins tasks executed by ``./manage.py jenkins`` command.

  Default value::

    JENKINS_TASKS = (
        'django_jenkins.tasks.run_pylint',
        'django_jenkins.tasks.with_coverage',
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

  Task-specific settings: ``PYLINT_RCFILE``

.. _Pylint: http://www.logilab.org/project/pylint

- ``django_jenkins.tasks.with_coverage``

  Produces `XML coverage report <http://nedbatchelder.com/code/coverage/sample_html/>`__ for Jenkins

  Task-specific settings: ``COVERAGE_RCFILE``, ``COVERAGE_REPORT_HTML_OUTPUT_DIR``, ``COVERAGE_MEASURE_BRANCH``, ``COVERAGE_EXCLUDES``, ``COVERAGE_WITH_MIGRATIONS``, ``COVERAGE_EXCLUDES_FOLDERS``

- ``django_jenkins.tasks.run_jshint``

  Runs jshint tools over ``<app>/static/*/*.js`` files.
  Creates Pylint compatible report for Jenkins

  You should have the jshint installed

- ``django_jenkins.tasks.run_csslint``

  Runs CSS lint tools over `app/static/*/*.css` files.
  Creates CSS Lint compatible report for Jenkins

  You should have the csslint installed

  Task-specific settings: ``CSSLINT_CHECKED_FILES``


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

- ``django_jenkins.tasks.run_graphmodels``

  Graphs an overview of the models of the selected Django apps.
  Creates ``models.png`` graphic (`example <https://code.djangoproject.com/wiki/DjangoGraphviz#Examples>`__).

  You should have django-extensions_ and pygraphviz_ installed to run this task.

  Task-specific settings:

  - ``GRAPH_MODELS``: A dictionary of settings for graph_models, most corresponding to the command-line options (with 'graphmodels\_' removed): ``fail_without_error``, ``disable_fields``, ``group_models``, ``all_applications``, ``outputfile``, ``layout``, ``verbose_names``, ``language``, ``exclude_columns``, ``exclude_models``, ``inheritance``

.. _django-extensions: http://pypi.python.org/pypi/django-extensions
.. _pygraphviz: http://pypi.python.org/pypi/pygraphviz/


- ``django_jenkins.tasks.with_local_celery``

  Replacement for ``djcelery.tests.runners.CeleryTestSuiteRunner``
  Change settings for run Celery_ tasks locally.

.. _Celery: http://ask.github.com/django-celery/


Changelog
---------

0.15.0 2013-02-15
~~~~~~~~~~~
* Speed up and reduced memory usage for junit reports generation
* django_tests and dir_tests test discovery tasks are replaced by directory discover test runner build-in in django 1.6
* Removed unmaintained lettuce tests support
* Removed unmaintained behave tests support
* Fixed non-asci support in junit reports


0.14.1 2013-08-15
~~~~~~~~~~~~~~~~~
* Django 1.6 compatibility
* Flake8 support
* Pep8 file configuration support
* CSSLint no longer shipped with django-jenkins. Install it with ``npm install csslint -g``


0.14.0 2012-12-15
~~~~~~~~~~~~~~~~~
* Python 3 (with django 1.5) support
* JSHint no longer shipped with django-jenkins. Install it with ``npm install jshint -g``


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


Contribution guide
~~~~~~~~~~~~~~~~~~

* Set up local jenkins
* Set up django-jenkins::

    npm install jshint
    npm install csslint
    PATH=$PATH:$WORKSPACE/node_modules/.bin
    tox -e $TOXENV

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

