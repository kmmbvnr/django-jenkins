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

Add django_hudson to your INSTALLED_APPS list.
Configure hudson to run the following command:

    $ ./manage.py jenkins

This will create reports/ directory with junit xml, coverage and pylint
reports.

For more details see the tutorial: http://sites.google.com/site/kmmbvnr/home/django-hudson-tutorial


Changelog
-------
django-jenkins 0.10.0 2010-02-15

   * Pluggable ci tasks refactoring
   * Alfa support for windmill tests
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

