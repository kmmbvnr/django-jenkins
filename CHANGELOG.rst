0.110.0 2016-09-15
~~~~~~~~~~~~~~~~~~

* Flake8 >= 3.0 support
* `scss-lint` task added

0.19.0 2016-06-15
~~~~~~~~~~~~~~~~~

* Flake8 >= 2.5.0 support
* Drop django 1.7 support
* Tested on django 1.10
* Add suppport for `.add_arguments` from custom test runner for `jenkins` command

0.18.0 1985-10-26
~~~~~~~~~~~~~~~~~

* An exceptional release for the last 5 years issued not on 15th day of a month
* Drop python 2.6 support
* Drop django 1.6 support
* Add django 1.9 compatibility
* Drop scss-lint support (the tool no longer have xml output)

0.17.0 2015-04-15
~~~~~~~~~~~~~~~~~~

* Django 1.8 compatibility
* Added support for excluding paths in the pyflakes runner
* --coverage-html-report option removed
* --coverage-format option added

0.16.4 2014-12-15
~~~~~~~~~~~~~~~~~

* New scss-lint task
* Added support for pylint plugins
* Include STATICFILES_DIRS to search path for csslint and jshint
* Search pep8 config in setup.cfg and tox.ini.
* Fix non-ascii tracback problem
* Fix error handlin in case exception happens in fixture loading
* Fix max-complexity option overriding

0.16.3 2014-08-15
~~~~~~~~~~~~~~~~~

* Python 2.6 compatibility returned
* Added `--project-apps-tests` options to limit tests discovery by `PROJECT_APPS` setting value
* Fix coverage for apps with separate models packages under django 1.6
* Fix missing pep8 excludes option from pep8 config


0.16.0 2014-07-15
~~~~~~~~~~~~~~~~~

* Django 1.7 compatibility
* Support for all standard django test runner options
* Migrations now our friends and checked by all linters, `south_migrations` are ignored
* ``django_jenkins.tasks.with_coverage`` depricated, use command line option instead `./manage.py jenkins --enable-coverage`
* ``django_jenkins.tasks.run_graphmodels`` removed
* ``django_jenkins.tasks.with_local_celery`` removed
* Ability to run linters (pep8/pyflakes/pylint/csslint/jshint) from command line without tests removed (feel free to PR it back, if you need them)


0.15.0 2014-02-15
~~~~~~~~~~~~~~~~~

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

