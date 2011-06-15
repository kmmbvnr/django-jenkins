# -*- coding: utf-8 -*-
import inspect
import sys
from optparse import make_option, OptionGroup
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.importlib import import_module
from django_jenkins import signals
from django_jenkins.runner import CITestSuiteRunner

def get_runner():
    if hasattr(settings, 'JENKINS_TEST_RUNNER'):
        test_path = settings.JENKINS_TEST_RUNNER.split('.')
        # Allow for Python 2.5 relative paths
        if len(test_path) > 1:
            test_module_name = '.'.join(test_path[:-1])
        else:
            test_module_name = '.'
        test_module = __import__(test_module_name, {}, {}, test_path[-1])
        test_runner = getattr(test_module, test_path[-1])

        if not issubclass(test_runner, CITestSuiteRunner):
            raise ValueError('Your custom TestRunner should extend the CITestSuiteRunner class.')
        return test_runner
    else:
        return CITestSuiteRunner


class TaskListCommand(BaseCommand):
    """
    Run list of predifined tasks from command line
    """
    requires_model_validation = False  # if True, breaks coverage of models.py files

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='test_all', default=False,
            help='Ignore PROJECT_APPS settings and run through all INSTALLED_APPS'),
        make_option('--interactive', action='store_true', dest='interactive', default=False,
            help='Allow to ask user input'),
        make_option('--debug', action='store_true', dest='debug', default=False,
            help='Do not intercept stdout and stderr, friendly for console debuggers'),
        make_option('--output-dir', dest='output_dir', default="reports",
            help='Report files directory'),
    )

    def __init__(self):
        super(TaskListCommand, self).__init__()
        self.tasks_cls = [import_module(module_name).Task for module_name in self.get_task_list()]

    def handle(self, *test_labels, **options):
        # instantiate tasks
        self.tasks = [task_cls(test_labels, options) for task_cls in self.tasks_cls]

        # subscribe
        for signal_name, signal in inspect.getmembers(signals):
            for task in self.tasks:
                signal_handler = getattr(task, signal_name, None)
                if signal_handler:
                    signal.connect(signal_handler)

        # run
        test_runner_cls = get_runner()
        test_runner = test_runner_cls(
            output_dir=options['output_dir'],
            interactive=options['interactive'],
            debug=options['debug'],
            verbosity=int(options.get('verbosity', 1)),
            with_reports=options.get('with_reports', True))

        if test_runner.run_tests(test_labels):
            sys.exit(1)

    def get_task_list(self):
        """
        Return list of task modules for command

        Subclasses should override this method
        """
        return []

    def create_parser(self, *args):
        """
        Extend the option list with tasks specific options
        """
        parser = super(TaskListCommand, self).create_parser(*args)

        for task_cls in self.tasks_cls:
            option_group = OptionGroup(parser, task_cls.__module__, "")

            if task_cls.option_list:
                for option in task_cls.option_list:
                    option_group.add_option(option)
                parser.add_option_group(option_group)

        return parser
