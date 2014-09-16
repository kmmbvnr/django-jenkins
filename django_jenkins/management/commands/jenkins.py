import os
import sys
import warnings
from optparse import OptionParser, make_option

from django.conf import settings
from django.core.management.commands.test import Command as TestCommand
from django.utils.importlib import import_module

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
    option_list = TestCommand.option_list + (
        make_option('--output-dir', dest='output_dir', default="reports",
                    help='Report files directory'),
        make_option("--enable-coverage",
                    action="store_true", default=False,
                    help="Measure code coverage"),
        make_option('--debug', action='store_true',
                    dest='debug', default=False,
                    help='Do not intercept stdout and stderr, friendly for console debuggers'),
        make_option("--coverage-rcfile",
                    dest="coverage_rcfile",
                    default="",
                    help="Specify configuration file."),
        make_option("--coverage-html-report",
                    dest="coverage_html_report_dir",
                    default="",
                    help="Directory to which HTML coverage report should be"
                    " written. If not specified, no report is generated."),
        make_option("--coverage-exclude", action="append",
                    default=[], dest="coverage_excludes",
                    help="Module name to exclude"),
        make_option("--project-apps-tests", action="store_true",
                    default=False, dest="project_apps_tests",
                    help="Take tests only from project apps")
    )

    def __init__(self):
        super(Command, self).__init__()
        self.tasks_cls = [import_module(module_name).Reporter
                          for module_name in self.get_task_list()]
        self.tasks = [task_cls() for task_cls in self.tasks_cls]

    def get_task_list(self):
        tasks = getattr(settings, 'JENKINS_TASKS', ())
        if '--enable-coverage' in sys.argv and 'django_jenkins.tasks.with_coverage' not in tasks:
            try:
                from django.apps import apps  # NOQA
            except ImportError:
                """
                We are on django 1.6
                """
                tasks += ('django_jenkins.tasks.with_coverage',)
        return tasks

    def create_parser(self, prog_name, subcommand):
        test_runner_class = get_runner(settings, self.test_runner)
        options = self.option_list + getattr(
            test_runner_class, 'option_list', ())

        for task in self.tasks:
            options += tuple(option for option in getattr(task, 'option_list', ())
                             if all(option._long_opts[0] != existing._long_opts[0]
                                    for existing in options))

        return OptionParser(prog=prog_name,
                            usage=self.usage(subcommand),
                            version=self.get_version(),
                            option_list=options)

    def handle(self, *test_labels, **options):
        TestRunner = get_runner(settings, options.get('testrunner'))
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

            # dump coverage
            try:
                from django.apps import apps
                coverage = apps.get_app_config('django_jenkins').coverage
                if coverage:
                    if options['verbosity'] >= 1:
                        print('Storing coverage info...')

                    coverage.save(tested_locations, options)
            except ImportError:
                """
                Do nothing on django 1.6
                """

            # run reporters
            for task in self.tasks:
                if options['verbosity'] >= 1:
                    print('Executing {0}...'.format(task.__module__))
                task.run(tested_locations, **options)

            if options['verbosity'] >= 1:
                print('Done')

    def get_tested_locations(self, test_labels):
        locations = []

        if test_labels:
            pass
        elif hasattr(settings, 'PROJECT_APPS'):
            test_labels = settings.PROJECT_APPS
        else:
            warnings.warn('No PROJECT_APPS settings, coverage gathered over all apps')
            test_labels = settings.INSTALLED_APPS

        try:
            from django.apps import apps
            for test_label in test_labels:
                app_config = apps.get_containing_app_config(test_label)
                if app_config is not None:
                    locations.append(os.path.dirname(app_config.module.__file__))
                else:
                    warnings.warn('No app found for test: {0}'.format(test_label))
        except ImportError:
            # django 1.6
            from django.utils.importlib import import_module

            def get_containing_app(object_name):
                candidates = []
                for app_label in settings.INSTALLED_APPS:
                    if object_name.startswith(app_label):
                        subpath = object_name[len(app_label):]
                        if subpath == '' or subpath[0] == '.':
                            candidates.append(app_label)
                if candidates:
                    return sorted(candidates, key=lambda label: -len(label))[0]

            for test_label in test_labels:
                app_label = get_containing_app(test_label)
                if app_label is not None:
                    app_module = import_module(app_label)
                    locations.append(os.path.dirname(app_module.__file__))
                else:
                    warnings.warn('No app found for test: {0}'.format(test_label))

        return locations
