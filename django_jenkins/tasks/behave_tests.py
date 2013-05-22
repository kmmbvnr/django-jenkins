"""
Build suite with behave tests
"""
from django.db.models import get_app
from django.conf import settings
from django_jenkins.tasks import BaseTask

from django_behave.runner import get_features, DjangoBehaveTestCase, make_test_suite


class Task(BaseTask):
    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        if not self.test_labels:
            if hasattr(settings, 'PROJECT_APPS') and not options['test_all']:
                self.test_labels = [app_name.split('.')[-1]
                                        for app_name in settings.PROJECT_APPS]

    def build_suite(self, suite, **kwargs):
        for label in self.test_labels:
            if '.' in label:
                print "Ignoring label with dot in: " % label
                continue
            app = get_app(label)
            
            # Check to see if a separate 'features' module exists,
            # parallel to the models module
            features_dir = get_features(app)
            if features_dir is not None:
                # build a test suite for this directory
                features_test_suite = make_test_suite(features_dir)
                suite.addTest(features_test_suite)
