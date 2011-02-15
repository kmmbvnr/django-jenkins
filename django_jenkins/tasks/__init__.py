# -*- coding: utf-8 -*-
from django.conf import settings

class BaseTask(object):
    """
    Base interface for ci tasks
    """
    option_list = []

    def __init__(self, test_labels, options):
        self.test_labels = test_labels

    def setup_test_environment(self, **kwargs):
        pass

    def teardown_test_environment(self, **kwargs):
        pass

    def before_suite_run(self, **kwargs):
        pass

    def after_suite_run(self, **kwargs):
        pass

    def build_suite(self, suite, **kwargs):
        pass


def get_apps_under_test(test_labels, all_apps=False):
    """
    Convert test_lables for apps names

    all_apps - if test_labels empty, ignore white list, 
    and returns all installed apps
    """
    if not test_labels:
        if hasattr(settings, 'PROJECT_APPS') and not all_apps:
            apps = settings.PROJECT_APPS
        else:
            apps = settings.INSTALLED_APPS
    else:
        apps = [app for app in settings.INSTALLED_APPS \
                    for label in test_labels \
                    if app == label.split('.')[0] or app.endswith('.%s' % label.split('.')[0])]
    return apps

