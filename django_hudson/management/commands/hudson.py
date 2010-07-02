# -*- coding: utf-8 -*-
import sys, os
from os import path
import coverage
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django_hudson.management.commands.lint import Command as pylint
from django_hudson.xmlrunner import XmlDjangoTestSuiteRunner

class Command(BaseCommand):
    help = "Run ci process"

    option_list = BaseCommand.option_list + (
        make_option('--output', dest='output_dir', default='reports',
                    help='Reports directory'),
    )

    def handle(self, *args, **options):
        """
        Run pylint and test with coverage and xml reports
        """
        output_dir=options.get('output_dir')

        os.mkdir(output_dir)

        app_labels = Command.app_list()

        # pylint
        pylint().handle(*app_labels, 
                         output_file=path.join(output_dir,'pylint.report'))


        #coverage
        coverage.exclude('#pragma[: ]+[nN][oO] [cC][oO][vV][eE][rR]')
        coverage.start()
        
        #tests
        test_runner = XmlDjangoTestSuiteRunner(output_dir=output_dir)
        failures = test_runner.run_tests(app_labels)

        #save coverage report
        coverage.stop()
        
        modules = [module for name, module in sys.modules.items() \
                       if module and any([name.startswith(label) for label in app_labels])]

        morfs = [ m.__file__ for m in modules if hasattr(m, '__file__') ]
        coverage._the_coverage.xml_report(morfs, outfile=path.join(output_dir,'coverage.xml'))

    @staticmethod
    def app_list():
        if hasattr(settings, 'PROJECT_APPS'):
            return settings.PROJECT_APPS
        return settings.INSTALLED_APPS

