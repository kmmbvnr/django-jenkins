# -*- coding: utf-8 -*-
import sys
from optparse import make_option
from django.core.management.base import BaseCommand
from django_hudson.xmlrunner import XmlDjangoTestSuiteRunner

try:
    import south
    try:
        from south.management.commands import patch_for_test_db_setup
    except Exception:
        #Just in case the south paths change, we want to fail fast and loud
        raise
except ImportError:
    #Must not have south
    def patch_for_test_db_setup():
        pass

class Command(BaseCommand):
    help = "Runs the test suite with reporting to xml"

    option_list = BaseCommand.option_list + (
        make_option('--output', dest='output_dir', default='',
                    help='Directory for xml report'),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
    )


    def handle(self, *test_labels, **options):
        patch_for_test_db_setup()
        output_dir=options.get('output_dir')
        
        verbosity = int(options.get('verbosity', 1))
        interactive = options.get('interactive', True)
        
        test_runner = XmlDjangoTestSuiteRunner(output_dir=output_dir, interactive=interactive, verbosity=verbosity)
        failures = test_runner.run_tests(test_labels)

        if failures:
            sys.exit(bool(failures))

