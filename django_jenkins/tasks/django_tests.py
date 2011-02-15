# -*- coding: utf-8 -*-
# pylint: disable=W0201, W0141
"""
Build suite with normal django tests
"""
from django.test.simple import build_suite, build_test
from django.db.models import get_app, get_apps
from django_jenkins.tasks import BaseTask


class Task(BaseTask):
    def build_suite(self, suite, **kwargs):
        if self.test_labels:
            for label in self.test_labels:
                if '.' in label:
                    suite.addTest(build_test(label))
                else:
                    app = get_app(label)
                    suite.addTest(build_suite(app))
        else:
            for app in get_apps():
                suite.addTest(build_suite(app))

