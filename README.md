# django-jenkins

Plug and play continuous integration with Django and Jenkins

## Installation

Using `pip`:

    pip install django-jenkins

Or by downloading the source and running:

    python setup.py install

Latest git version:

    pip install -e git+git://github.com/kmmbvnr/django-jenkins.git#egg=django-jenkins
    pip install coverage

## Usage

Add `django_jenkins` to your `INSTALLED_APPS` list.
Configure Jenkins to run the following command:

    ./manage.py jenkins --enable-coverage

This will create a reports directory with junit `junit.xml`, coverage `coverage.xml` and pylint `pylint.xml`
reports.

## Settings

- `PROJECT_APPS`

  If present, it is supposed to be a list or tuple of django apps for Jenkins to run.
  Tests, reports, and coverage are generated only for the apps from this list.

- `JENKINS_TASKS`

  List of Jenkins reporters executed by `./manage.py jenkins` command.

  Default value: `JENKINS_TASKS = ()`

- `JENKINS_TEST_RUNNER`

  The name of the class to use for starting the test suite for `jenkins` command.

  Class should be inherited from
  `django_jenkins.runner.CITestSuiteRunner`

## Reporters

A list of packaged reporters

- `django_jenkins.tasks.run_pylint`

  Runs [Pylint](http://www.logilab.org/project/pylint)

  Creates a Pylint (`pylint.report`) report

  Task-specific settings: ``PYLINT_RCFILE``

- `django_jenkins.tasks.run_csslint`

  Runs [csslint](https://github.com/CSSLint/csslint) tools over `app/static/*/*.css` files.

  Creates a CSS Lint (`csslint.report`) report

  You will need the `csslint` node package installed:

      sudo npm install csslint -g

- `django_jenkins.tasks.run_jshint`

  Runs [jshint](http://jshint.com/) tools over `<app>/static/*/*.js` files.

  Creates a JSHint report (`jshint.report`)

  You will need the `jshint` node package installed:

      sudo npm install jshint -g

- `django_jenkins.tasks.run_pep8`

  Runs [pep8](http://pypi.python.org/pypi/pep8)

  Creates a pep8 report (`pep8.report`)

  You will need the `pep8` python package (>=1.3) installed:

      pip install pep8

  Task-specific settings: `PEP8_RCFILE`

- `django_jenkins.tasks.run_pyflakes`

  Runs [pyflakes](http://pypi.python.org/pypi/pyflakes)

  Creates a pyflakes report (`pyflakes.report`)

  You will need the `pyflakes` python package installed:

      pip install pyflakes

- `django_jenkins.tasks.run_flake8`

  Runs [flake8](http://pypi.python.org/pypi/flake8)

  Creates a flake8 report (`flake8.report`)

  You will need the `flake8` python package installed:

- `django_jenkins.tasks.run_sloccount`

  Runs [SLOCCount](http://www.dwheeler.com/sloccount/)

  Creates a sloccount plugin report ('sloccount.report')

  You should have the SLOCCount program installed to run this task.
