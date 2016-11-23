Getting started
===============

There are a lot of ways to enable continuous integration with your django project. But most of them require a lot of time to configure and setup ci server and make changes in your django project.

This tutorial introduces a new way to enable continuous integration for django project, with minimal projects modifications by means of with django-jenkins.

Previously, ad-hoc integration django with jenkins required using nose testing frameworks instead of django native unittests.  Since nose project uses custom test loader it leads to a lot of problems with django code - duplicate signals subscriptions, module loading and other test-only realted errors. Django-jenkins uses the standard unnittest runner, so the code under test works like in production. No difference between django-jenkins run and manage.py tests keeps your hands free for real work.

Configuring django project
--------------------------

To enable django_jenkins you need only to add ``django_jenkins`` to ``INSTALLED_APPS`` in ``settings.py``.

Running 

    $ python manage.py jenkins 

will do the same job as 

    $ python manage.py tests

but also will create reports folder in the root of your django project with jenkins parsable pylint, test coverage and tests reports.

Django-jenkins have support for several other testing tools/ To enable it, you should include tools task to ``JENKINS_TASKS`` settings variable.

    JENKINS_TASKS = (
        'django_jenkins.tasks.run_pep8',
        'django_jenkins.tasks.run_pyflakes',
        'django_jenkins.tasks.run_jslint',
        'django_jenkins.tasks.run_csslint',    
        'django_jenkins.tasks.run_sloccount'
    )

Please, note that corresponding task tool should be installed on jenkins server manually. Please refer to `django-jenkins README<https://github.com/kmmbvnr/django-jenkins/blob/master/README.rst>` for specific task dependencies list.

In order to get the right coverage, 'django_jenkins' app should be included as early as possible in `INSTALLED_APPS`

This tutorial doesn't cover the library dependency management and deployind your django project on external server. Basically you could setup the CI server as you did in your local environment.

But if you prefer automatically installation and configuration dependencies on CI server, you could easily add `virtalenv<http://pypi.python.org/pypi/virtualenv>` support for your project.

Add to you project file named requirements.pip with all project dependencies list

    Django
    django-jenkins
    # any other libraries for your project

Running

    $ virtualenv --python=python2.6 env
    $ env/bin/pip install -r requirements.pip

will create local folder env with the required libraries for your project. Running those commands on other servers will help to sync the external dependencies.


Configuring jenkins
-------------------

After a fresh `Jenkins<http://jenkins-ci.org/>` installation, you'll need to install two required plugins: **`Violations<https://wiki.jenkins-ci.org/display/JENKINS/Violations>`** plugin for parsing ``pylint`` reports and **`Cobertura<http://www.mojohaus.org/cobertura-maven-plugin/>`** Plugin for showing the code coverage. Install these plugins via ``Manage Jenkins -> Manage Plugins -> Available``.

Start new job with creating free-style project:

.. image:: jenkins-1-newjob.jpg

After configuring the repository access, set up the build trigers. Poll SCM will run the build if any changes in repository are found. The line ``*/5 * * * *`` means checking repository every 5 minutes.

.. image:: 2_poll_scm.png

Select ``Add build step -> Execute shell``. Add comands to setup environment and the run tests command

    $ python manage.py jenkins --enable-coverage

	.. image:: jenkins-2.png

Specify the location of test reports - ``reports/TEST-*.xml`` and ``reports/lettuce.xml`` (in case you are using lettuce tests) files.

**CHANGED in 0.13.0:**: test reports from ``TEST-*.xml`` now stored in one file: ``junit.xml``.

.. image:: jenkins-3.png

Configure locations of violations reports:

.. image:: jenkins-4.png

Test coverage reports are in ``reports/coverage.xml``

.. image:: 6_coverage.png

That's all!

Results
-------

Press ``Build Now`` and see what you've got:

``Pylint`` and other lint tools reports for each builds, shows what warning/errors are new for each build.

.. image:: jenkins-5.png

Nice code coverage reports, showing the total coverage, and colored file listing.

.. image :: 8_coverage_results.png

And of course the test results and output.

.. image:: jenkins-6.png

