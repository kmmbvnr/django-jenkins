import os
import sys
import warnings
from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.core.management.commands.test import Command as TestCommand

from django_jenkins.runner import CITestSuiteRunner


def get_runner(settings, test_runner_class=None):
    if test_runner_class is None:
        test_runner_class = getattr(
            settings, 'JENKINS_TEST_RUNNER', 'django_jenkins.runner.CITestSuiteRunner')

    test_module_name, test_cls = test_runner_class.rsplit('.', 1)
    test_module = __import__(test_module_name, {}, {}, test_cls)
    test_runner = getattr(test_module, test_cls)

    if not issubclass(test_runner, CITestSuiteRunner):
        raise ValueError('Your custom TestRunner should extend '
                         'the CITestSuiteRunner class.')
    return test_runner


class Command(TestCommand):
    def __init__(self):
        self.test_runner = None
        self.tasks_cls = [import_module(module_name).Reporter
                          for module_name in self.get_task_list()]
        self.tasks = [task_cls() for task_cls in self.tasks_cls]
        super(Command, self).__init__()

    def run_from_argv(self, argv):
        """
        Pre-parse the command line to extract the value of the --testrunner
        option. This allows a test runner to define additional command line
        arguments.
        """
        option = '--testrunner='
        for arg in argv[2:]:
            if arg.startswith(option):
                self.test_runner = arg[len(option):]
                break
        super(Command, self).run_from_argv(argv)

    def get_task_list(self):
        return getattr(settings, 'JENKINS_TASKS', ())

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--output-dir', dest='output_dir', default="reports",
                            help='Report files directory'),
        parser.add_argument("--enable-coverage",
                            action="store_true", default=False,
                            help="Measure code coverage"),
        parser.add_argument('--debug', action='store_true',
                            dest='debug', default=False,
                            help='Do not intercept stdout and stderr, friendly for console debuggers'),
        parser.add_argument("--coverage-rcfile",
                            dest="coverage_rcfile",
                            default="",
                            help="Specify configuration file."),
        parser.add_argument("--coverage-format",
                            dest="coverage_format",
                            default="xml",
                            help="Specify coverage output formats html,xml,bin"),
        parser.add_argument("--coverage-exclude", action="append",
                            default=[], dest="coverage_excludes",
                            help="Module name to exclude"),
        parser.add_argument("--project-apps-tests", action="store_true",
                            default=False, dest="project_apps_tests",
                            help="Take tests only from project apps")

        parser._optionals.conflict_handler = 'resolve'
        for task in self.tasks:
            if hasattr(task, 'add_arguments'):
                task.add_arguments(parser)

        test_runner_class = get_runner(settings, self.test_runner)

        if hasattr(test_runner_class, 'add_arguments'):
            test_runner_class.add_arguments(parser)

    def handle(self, *test_labels, **options):
        TestRunner = get_runner(settings, options['testrunner'])
        options['verbosity'] = int(options.get('verbosity'))

        if options.get('liveserver') is not None:
            os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = options['liveserver']
            del options['liveserver']

        output_dir = options['output_dir']
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        test_runner = TestRunner(**options)

        if not test_labels and options['project_apps_tests']:
            test_labels = getattr(settings, 'PROJECT_APPS', [])

        failures = test_runner.run_tests(test_labels)

        if failures:
            sys.exit(bool(failures))
        else:
            tested_locations = self.get_tested_locations(test_labels)

            coverage = apps.get_app_config('django_jenkins').coverage
            if coverage:
                if options['verbosity'] >= 1:
                    print('Storing coverage info...')

                coverage.save(tested_locations, options)

            # run reporters
            for task in self.tasks:
                if options['verbosity'] >= 1:
                    print('Executing {0}...'.format(task.__module__))
                task.run(tested_locations, **options)

            if options['verbosity'] >= 1:
                print('Done')

    def get_tested_locations(self, test_labels):
        locations = []

        coverage = apps.get_app_config('django_jenkins').coverage
        if test_labels:
            pass
        elif hasattr(settings, 'PROJECT_APPS'):
            test_labels = settings.PROJECT_APPS
        elif coverage and coverage.coverage.source:
            warnings.warn("No PROJECT_APPS settings, using 'source' config from rcfile")
            locations = coverage.coverage.source
        else:
            warnings.warn('No PROJECT_APPS settings, coverage gathered over all apps')
            test_labels = settings.INSTALLED_APPS

        for test_label in test_labels:
            app_config = apps.get_containing_app_config(test_label)
            if app_config is not None:
                locations.append(app_config.path)
            else:
                warnings.warn('No app found for test: {0}'.format(test_label))

        return locations
