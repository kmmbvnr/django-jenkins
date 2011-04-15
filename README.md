django-jenkins
=============

Plug and play continuous integration with django and jenkins

Installation
------------

    $ python setup.py install

    Or, for the latest git version

    $ pip install -e git://github.com/kmmbvnr/django-jenkins.git#egg=django-jenkins


Usage
-----

Add django_jenkins to your INSTALLED_APPS list.
Configure jenkins to run the following command:

    $ ./manage.py jenkins

This will create reports/ directory with junit xml, coverage and pylint
reports.

For more details see the tutorial: http://sites.google.com/site/kmmbvnr/home/django-hudson-tutorial

Settings
--------

### `PROJECT_APPS`
if presents, it is supposed to be a white list of apps for jenkins run.
Tests, reports and coverage are generated only for the apps from this list.
You should specify --all option to ignore this settings.

### `JENKINS_TASKS`

List of jenkins tasks executed by ./manage.py jenkins command.

Default value:

    JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                     'django_jenkins.tasks.with_coverage',
                     'django_jenkins.tasks.django_tests',)

### `JENKINS_TEST_RUNNER`
The name of the class to use for starting the test suite for `jenkins` and `jtest` commands.
Class should be inherited from `django_jenkins.runner.CITestSuiteRunner`

Tasks
-----

Here is the list of tasks prebuild with django-jenkins

### `django_jenkins.tasks.run_pylint`

Runs pylint over selected django apps.

### `django_jenkins.tasks.with_coverage`

Produces xml coverage report for jenkinx

### `django_jenkins.tasks.django_tests`

Discovers standard django test suite from test.py files

### `django_jenkins.tasks.run_jslint`

Runs jslint tools over `app/static/*/*.js` files. 
Creates pylint compatible report for jenkins

You should have `rhino` javascript interpreter installed for jslint

### `django_jenkins.tasks.run_pep8`

Runs pep8 tool over selected django apps.
Creates pylint compatible report for jenkins

You should have pep8 python package installed to run this tasks

### `django_jenkins.tasks.run_pyflakes`

Runs pyflakes tool over selected django apps.
Creates pylint compatible report for jenkins.

You should have pyflakes python package installed to run this tasks

### `django_jenkins.tasks.windmill_tests`

Discover windmill tests from app/wmtests.py files.
Each tests should be inherited from `django_jenkins.tasks.windmill_tests.WindmillTestCase`

You should have windmill python package installed to run this tasks

Changelog
-------
django-jenkins 0.11.0 2010-04-15

   * Suuport pep8, pyflakes, jslint tools
   * Added jtest command
   * Allow specify custom test runner
   * Various fixes, thnk githubbers :)

django-jenkins 0.10.0 2010-02-15

   * Pluggable ci tasks refactoring
   * Alpha support for windmill tests
   * Partial python 2.4 compatibility
   * Renamed to django-jenkins

django-hudson 0.9.1 2010-12-15

   * Python 2.5 compatibility
   * Make compatible with latest pylint only

django-hudson 0.9.0 2010-10-15

   * Initial public release


Authors
-------
Mikhail Podgurskiy <kmmbvnr@gmail.com>

Special thanks, for all github forks authors.

XML Reporting Code from unittest-xml-reporting project:
    Name:    Daniel Fernandes Martins <daniel.tritone@gmail.com>
    Company: Destaquenet Technology Solutions <http://www.destaquenet.com/>

