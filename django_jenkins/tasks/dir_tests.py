# -*- coding: utf-8 -*-
"""
Discover tests from all test*.py files in app subdirectories
"""
import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app, get_apps
from django.test.simple import build_test
from django.utils.unittest import defaultTestLoader
from django_jenkins.tasks import BaseTask, get_app_location


def build_suite(app):
    discovery_root = get_app_location(app)
    top_level_dir = discovery_root
    for _ in range(0, app.__name__.count('.')):
        top_level_dir = os.path.dirname(top_level_dir)
    return defaultTestLoader.discover(discovery_root, top_level_dir=top_level_dir)


class Task(BaseTask):
    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        if not self.test_labels:
            if hasattr(settings, 'PROJECT_APPS') and not options['test_all']:
                self.test_labels = [app_name.split('.')[-1] for app_name in settings.PROJECT_APPS]

    def build_suite(self, suite, **kwargs):
        if self.test_labels:
            for label in self.test_labels:
                if '.' in label:
                    suite.addTest(build_test(label))
                else:
                    try:
                        app = get_app(label)
                        suite.addTest(build_suite(app))
                    except ImproperlyConfigured:
                        pass
        else:
            for app in get_apps():
                suite.addTest(build_suite(app))

