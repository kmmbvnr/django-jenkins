import sys
from django.apps import AppConfig
from django_jenkins.tasks.with_coverage import CoverageReporter


class JenkinsConfig(AppConfig):
    """
    Enable coverage measurement as soon as possible
    """
    name = 'django_jenkins'

    def __init__(self, app_name, app_module):
        super(JenkinsConfig, self).__init__(app_name, app_module)

        self.coverage = None

        if 'jenkins' in sys.argv and '--enable-coverage' in sys.argv:
            """
            Starting coverage as soon as possible
            """
            self.coverage = CoverageReporter()
