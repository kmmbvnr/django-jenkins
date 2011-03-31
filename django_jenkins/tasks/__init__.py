# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.db.models import get_app

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


def get_apps_locations(test_labels, all_apps=False):
    """
    Returns list of paths to tested apps
    """
    return [os.path.dirname(get_app(app_name.split('.')[-1]).__file__) \
            for app_name in get_apps_under_test(test_labels, all_apps)]

