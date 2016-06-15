from django_jenkins.runner import CITestSuiteRunner


class CustomTestRunner(CITestSuiteRunner):
    @classmethod
    def add_arguments(self, parser):
        parser.add_argument('--ok', default=False, action='store_true', help='Custom test runner option')
