import os
import sys
from importlib import import_module

from django.conf import settings


class CoverageReporter(object):
    def __init__(self):
        try:
            import coverage
        except ImportError:
            raise ImportError('coverage is not installed')

        if coverage.__version__ < '4':
            raise ImportError('coverage>=4 required')

        coverage_config_file = None
        for argv in sys.argv:
            if argv.startswith('--coverage-rcfile='):
                _, coverage_config_file = argv.split('=')

        self.coverage = coverage.coverage(
            branch=True,
            config_file=coverage_config_file or self.default_coverage_config())
        self.coverage.start()

    def save(self, apps_locations, options):
        self.coverage.stop()
        self.coverage.get_data()
        morfs = self.get_morfs(self.coverage, apps_locations, options)

        if 'xml' in options['coverage_format']:
            self.coverage.xml_report(morfs=morfs, outfile=os.path.join(options['output_dir'], 'coverage.xml'))
        if 'bin' in options['coverage_format']:
            self.coverage.save()
        if 'html' in options['coverage_format']:
            # Dump coverage html
            self.coverage.html_report(morfs=morfs, directory=os.path.join(options['output_dir'], 'coverage'))

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

    def default_coverage_config(self):
        rcfile = getattr(settings, 'COVERAGE_RCFILE', 'coverage.rc')
        if os.path.exists(rcfile):
            return rcfile
        return None
