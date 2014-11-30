import warnings
import os
import sys
from django.conf import settings
from django.utils.importlib import import_module


def default_coverage_config():
    rcfile = getattr(settings, 'COVERAGE_RCFILE', 'coverage.rc')
    if os.path.exists(rcfile):
        return rcfile
    return None


class CoverageReporter(object):
    def __init__(self):
        try:
            from coverage import coverage
        except ImportError:
            raise ImportError('coverage is not installed')
        else:
            coverage_config_file = None
            for argv in sys.argv:
                if argv.startswith('--coverage-rcfile='):
                    _, coverage_config_file = argv.split('=')

            self.coverage = coverage(
                branch=True,
                config_file=coverage_config_file or default_coverage_config())
            self.coverage.start()

    def save(self, apps_locations, options):
        self.coverage.stop()
        self.coverage._harvest_data()
        morfs = self.get_morfs(self.coverage, apps_locations, options)

        self.coverage.xml_report(morfs=morfs, outfile=os.path.join(options['output_dir'], 'coverage.xml'))

        # Dump coverage html
        coverage_html_dir = options.get('coverage_html_report_dir') \
            or getattr(settings, 'COVERAGE_REPORT_HTML_OUTPUT_DIR', '')
        if coverage_html_dir:
            self.coverage.html_report(morfs=morfs, directory=coverage_html_dir)

    def get_morfs(self, coverage, tested_locations, options):
        excluded = []

        # Exclude by module
        modnames = options.get('coverage_excludes') or getattr(settings, 'COVERAGE_EXCLUDES', [])
        for modname in modnames:
            try:
                excluded.append(os.path.dirname(import_module(modname).__file__))
            except ImportError:
                pass

        # Exclude by directory
        excluded.extend(getattr(settings, 'COVERAGE_EXCLUDES_FOLDERS', []))

        return [filename for filename in coverage.data.measured_files()
                if not (os.sep + 'migrations' + os.sep) in filename
                if not (os.sep + 'south_migrations' + os.sep) in filename
                if any(filename.startswith(location) for location in tested_locations)
                if not any(filename.startswith(location) for location in excluded)]


class Reporter(object):
    def __init__(self):
        try:
            from django.apps import apps
            self.coverage_reporter = apps.get_app_config('django_jenkins').coverage
            if self.coverage_reporter is None:
                warnings.warn('django_jenkins.tasks.with_coverage is depricated.'
                              ' Please, delete it from JENKINS_TASKS and use --enable-coverage'
                              ' command line option instead')
                self.coverage_reporter = CoverageReporter()
        except ImportError:
            # Ok, on django 1.6 work as usual
            self.coverage_reporter = CoverageReporter()

    def run(self, apps_locations, **options):
        self.coverage_reporter.save(apps_locations, options)
