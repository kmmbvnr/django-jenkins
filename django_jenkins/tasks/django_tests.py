# -*- coding: utf-8 -*-
# pylint: disable=W0201, W0141
"""
Build suite with normal django tests
"""
from django.test.simple import build_suite, build_test
from django.db.models import get_app, get_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django_jenkins.tasks import BaseTask


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
