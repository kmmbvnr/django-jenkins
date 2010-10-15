django-hudson
=============

Plug and play continuous integration with django and hudson

Installation
------------

    $ python setup.py install

    Or, for the latest git version

    $ pip install -e git://github.com/kmmbvnr/django-hudson.git#egg=django-hudson


Usage
-----

Add django_hudson to your INSTALLED_APPS list.
Configure hudson to run the following command:

    $ ./manage.py hudson

This will create reports/ directory with junit xml, coverage and pylint
reports.

For more details see the tutorial: http://sites.google.com/site/kmmbvnr/home/django-hudson-tutorial

Authors
-------
Mikhail Podgurskiy <kmmbvnr@gmail.com>

Special thanks, for all github forks authors.
This release contains some patches from:
     Chris Heisel <http://heisel.org>
     http://github.com/cmheisel/django-hudson

XML Reporting Code from unittest-xml-reporting project:
    Name:    Daniel Fernandes Martins <daniel.tritone@gmail.com>
    Company: Destaquenet Technology Solutions <http://www.destaquenet.com/>

