# -*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand
from django_hudson.xmlrunner import XmlDjangoTestSuiteRunner

class Command(BaseCommand):
    help = "Runs the test suite with reporting to xml"

    option_list = BaseCommand.option_list + (
        make_option('--output', dest='output_dir', default='',
                    help='Directory for xml report'),
    )


    def handle(self, *test_labels, **options):
        output_dir=options.get('output_dir')
        
        test_runner = XmlDjangoTestSuiteRunner(output_dir=output_dir)
        failures = test_runner.run_tests(test_labels)

        if failures:
            sys.exit(bool(failures))

