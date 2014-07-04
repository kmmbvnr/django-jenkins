import os
import sys
import warnings
from optparse import OptionParser, make_option


from django.apps import apps
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
                    help="Module name to exclude")
    )

    def __init__(self):
        super(Command, self).__init__()
        self.tasks_cls = [import_module(module_name).Reporter
                          for module_name in self.get_task_list()]
        self.tasks = [task_cls() for task_cls in self.tasks_cls]

    def get_task_list(self):
        return getattr(settings, 'JENKINS_TASKS',
                       ('django_jenkins.tasks.run_pep8',))

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
        failures = test_runner.run_tests(test_labels)

        if failures:
            sys.exit(bool(failures))
        else:
            tested_locations = self.get_tested_locations(test_labels)

            # Dump coverage
            coverage = apps.get_app_config('django_jenkins').coverage
            if coverage:
                if options['verbosity'] >= 1:
                    print('Storing coverage info..')

                coverage.stop()
                coverage._harvest_data()
                morfs = self.get_morfs(coverage, tested_locations, options)

                coverage.xml_report(morfs=morfs, outfile=os.path.join(options['output_dir'], 'coverage.xml'))

                # Dump coverage html
                coverage_html_dir = options.get('coverage_html_report_dir') \
                    or getattr(settings, 'COVERAGE_REPORT_HTML_OUTPUT_DIR', '')
                if coverage_html_dir:
                    coverage.html_report(morfs=morfs, directory=coverage_html_dir)

            # Run reporters
            for task in self.tasks:
                if options['verbosity'] >= 1:
                    print('Excuting {}...'.format(task.__module__))
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
            warnings.warn('No PROJECTS_APPS settings, coverage gathered over all apps')
            test_labels = settings.INSTALLED_APPS

        for test_label in test_labels:
            app_config = apps.get_containing_app_config(test_label)
            locations.append(os.path.dirname(app_config.module.__file__))

        return locations

    def get_morfs(self, coverage, tested_locations, options):
        excluded = []

        # Exclude by module
        modnames = options.get('coverage_excludes') or getattr(settings, 'COVERAGE_EXCLUDES', [])
        for modname in modnames:
            try:
                excluded.append(
                    os.path.dirname(import_module(modname).__file__))
            except ImportError:
                pass

        # Exclude by directory
        excluded.extend(getattr(settings, 'COVERAGE_EXCLUDES_FOLDERS', []))

        return [filename for filename in coverage.data.measured_files()
                if any(filename.startswith(location) for location in tested_locations)
                if not any(filename.startswith(location) for location in excluded)]
