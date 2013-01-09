# -*- coding: utf-8 -*-
"""
Discover tests via the nose collector
"""
from django_jenkins.tasks import BaseTask


class Task(BaseTask):

    def build_suite(self, suite, **kwargs):
        import nose
        suite.addTest(nose.collector())
