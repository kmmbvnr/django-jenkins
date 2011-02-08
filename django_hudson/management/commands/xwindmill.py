# -*- coding: utf-8 -*-
import sys
from optparse import make_option, OptionGroup
from django.conf import settings
from django.core.management.base import BaseCommand
from django_hudson.tasks.run_windmill import Task as RunWindmill

class Command(BaseCommand):
    help = "Run windmill unittests"
    requires_model_validation = False

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_false', dest='test_all', default=True,
            help='Ignore PROJECT_APPS settings and test all INSTALLED_APPS'),
        make_option('--output-dir', dest='output_dir', default="reports",
            help='Report files directory'),
    )

    def handle(self, *test_labels, **options):
        task = RunWindmill()
        
        # handle all, or whitelisted apps
        if not test_labels:
            test_modules = settings.INSTALLED_APPS
            if hasattr(settings, 'PROJECT_APPS') and not options['test_all']:
                test_modules = settings.PROJECT_APPS
        else:
            test_modules = [app for app in settings.INSTALLED_APPS \
                                for label in test_labels \
                                if app == label or app.endswith('.%s' % label)]

        task.configure(test_modules, options)
        succeed=task.run_task()
        task.after_tasks_run()

        if not succeed:
            sys.exit(1)

    def create_parser(self, *args):
        # extend the option list with tasks specific options
        parser = super(Command, self).create_parser(*args)

        task = RunWindmill()
        option_group = OptionGroup(parser, task.__module__, "")
        task.add_options(option_group)
        if option_group.option_list:
            parser.add_option_group(option_group)
        return parser

