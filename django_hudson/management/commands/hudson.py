# -*- coding: utf-8 -*-
import sys, os
from os import path
from optparse import make_option, OptionGroup
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.importlib import import_module


class Command(BaseCommand):
    help = "Run CI process"
    args = '[appname ...]'
    requires_model_validation = False

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_false', dest='test_all', default=True,
            help='Ignore PROJECT_APPS settings and test all INSTALLED_APPS'),
        make_option('--output-dir', dest='output_dir', default="reports",
            help='Report files directory'),
    )

    def __init__(self):
        tasks_names = getattr(settings, 'HUDSON_TASKS',
                               ('django_hudson.tasks.run_pylint',
                                'django_hudson.tasks.with_coverage',
                                'django_hudson.tasks.run_xmltest',))
        self.tasks = [import_module(module_name).Task() for module_name in tasks_names]

    def handle(self, *test_labels, **options):
        output_dir=options['output_dir']
        if not path.exists(output_dir):
            os.makedirs(output_dir)

        # handle all, or whitelisted apps
        if not test_labels:
            test_modules = settings.INSTALLED_APPS
            if hasattr(settings, 'PROJECT_APPS') and not options['test_all']:
                test_modules = settings.PROJECT_APPS
        else:
            test_modules = [app for app in settings.INSTALLED_APPS \
                                for label in test_labels \
                                if app == label or app.endswith('.%s' % label)]

        # configure
        for task in self.tasks:
            task.configure(test_modules, options)

        # run_suite
        succeed = True
        for task in self.tasks:
            if not task.run_task():
                succeed = False

        # after_tasks_run
        for task in self.tasks:
            task.after_tasks_run()

        if not succeed:
            sys.exit(1)

    def create_parser(self, *args):
        # extend the option list with tasks specific options
        parser = super(Command, self).create_parser(*args)

        for task in self.tasks:
            option_group = OptionGroup(parser, task.__module__, "")
            task.add_options(option_group)
            if option_group.option_list:
                parser.add_option_group(option_group)
        return parser

