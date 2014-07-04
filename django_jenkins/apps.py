import os
import sys
from django.apps import AppConfig
from django.conf import settings


def default_coverage_config():
    rcfile = getattr(settings, 'COVERAGE_RCFILE', 'coverage.rc')
    if os.path.exists(rcfile):
        return rcfile
    return None


class JenkinsConfig(AppConfig):
    """
    Enable coverage measurement as soon as possible
    """
    name = 'django_jenkins'

    def __init__(self, app_name, app_module):
        super(JenkinsConfig, self).__init__(app_name, app_module)

        self.coverage = None

        coverage_config_file = None
        if 'jenkins' in sys.argv and '--enable-coverage' in sys.argv:
            try:
                from coverage.control import coverage
            except ImportError:
                raise ImportError('coverage is not installed')
            else:
                for argv in sys.argv:
                    if argv.startswith('--coverage-rcfile='):
                        _, coverage_config_file = argv.split('=')

                self.coverage = coverage(
                    branch=True,
                    config_file=coverage_config_file or default_coverage_config())
                self.coverage.start()
