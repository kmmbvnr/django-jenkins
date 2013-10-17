# -*- coding: utf-8 -*-
# pylint: disable=W0201
import os
from optparse import make_option
from coverage.control import coverage
from django.conf import settings
from django.utils.importlib import import_module
from django_jenkins.tasks import BaseTask, get_apps_under_test


class Task(BaseTask):
    option_list = [
           make_option("--coverage-rcfile",
                       dest="coverage_rcfile",
                       default="",
               help="Specify configuration file."),
           make_option("--coverage-html-report",
                       dest="coverage_html_report_dir",
                       default="",
               help="Directory to which HTML coverage report should be"
                    " written. If not specified, no report is generated."),
           make_option("--coverage-no-branch-measure",
                       action="store_false", default=True,
                       dest="coverage_measure_branch",
               help="Don't measure branch coverage."),
           make_option("--coverage-with-migrations",
                       action="store_true", default=False,
                       dest="coverage_with_migrations",
               help="Don't measure migrations coverage."),
           make_option("--coverage-exclude", action="append",
                       default=[], dest="coverage_excludes",
               help="Module name to exclude")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_apps = get_apps_under_test(test_labels, options['test_all'])
        self.output_dir = options['output_dir']
        self.with_migrations = options.get('coverage_with_migrations',
                                    getattr(settings,
                                            'COVERAGE_WITH_MIGRATIONS', False))

        self.html_dir = options.get('coverage_html_report_dir') or \
                            getattr(settings,
                                    'COVERAGE_REPORT_HTML_OUTPUT_DIR', '')

        self.branch = options.get('coverage_measure_branch',
                                  getattr(settings,
                                          'COVERAGE_MEASURE_BRANCH', True))

        self.exclude_locations = []
        modnames = options.get('coverage_excludes') or \
                        getattr(settings, 'COVERAGE_EXCLUDES', [])
        for modname in modnames:
            try:
                self.exclude_locations.append(
                        os.path.dirname(
                            import_module(modname).__file__
                        )
                )
            except ImportError:
                pass

        # Extra folders to exclude. Particularly useful to specify things like
        # apps/company/migrations/*
        self.exclude_locations.extend(
                        getattr(settings, 'COVERAGE_EXCLUDES_FOLDERS', []))

        omit = self.exclude_locations
        if not omit:
            omit = None

        self.coverage = coverage(branch=self.branch,
                                 source=self.test_apps,
                                 omit=omit,
                                 config_file=options.get('coverage_rcfile') or
                                                 Task.default_config_path())

    def setup_test_environment(self, **kwargs):
        self.coverage.start()

    def teardown_test_environment(self, **kwargs):
        self.coverage.stop()
        self.coverage._harvest_data()
        morfs = [filename for filename in self.coverage.data.measured_files()
                 if self.want_file(filename)]

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.coverage.xml_report(morfs=morfs,
                                 outfile=os.path.join(
                                        self.output_dir, 'coverage.xml'))

        if self.html_dir:
            self.coverage.html_report(morfs=morfs, directory=self.html_dir)

    def want_file(self, filename):
        if not self.with_migrations and (os.sep + 'migrations' + os.sep) in filename:
            return False
        for location in self.exclude_locations:
            if filename.startswith(location):
                return False

        return True

    @staticmethod
    def default_config_path():
        rcfile = getattr(settings, 'COVERAGE_RCFILE', 'coverage.rc')
        if os.path.exists(rcfile):
            return rcfile
        return None
