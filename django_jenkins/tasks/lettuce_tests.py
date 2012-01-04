# -*- coding: utf-8 -*-
from os import path
from optparse import make_option
from django.conf import settings
from django_jenkins.tasks import BaseTask
from unittest import TestCase
from lettuce.django import harvest_lettuces
from lettuce import Runner
from lettuce import registry

class Task(BaseTask):
    option_list = [
        make_option("--lettuce-server",
               dest="lettuce-server",
               help="do not start runserver for lettuce tests",
               default=False),
    ]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        if not self.test_labels:
            if hasattr(settings, 'PROJECT_APPS') and not options['test_all']:
                self.test_labels = [app_name.split('.')[-1] for app_name in settings.PROJECT_APPS]

        self.lettuce_server = options['lettuce-server']
        self.output_dir = options['output_dir']

    def setup_test_environment(self, **kwargs):
        if self.lettuce_server:
            from lettuce.django import server
            self.server = server
            self.server.start()

    def teardown_test_environment(self, **kwargs):
        if self.lettuce_server:
            self.server.stop()

    def build_suite(self, suite, **kwargs):
        paths = harvest_lettuces(self.test_labels)
        for app_path, app_module in paths:
            runner = Runner(app_path,
                            enable_xunit=True,
                            xunit_filename=path.join(self.output_dir, 'lettuce.xml'))

            suite.addTest(LettuceTestCase(runner, app_module))

        return suite

class LettuceTestCase(TestCase):

    def __init__(self, runner, app_module, *args, **kwargs):
        super(LettuceTestCase, self).__init__(*args, **kwargs)
        self.runner = runner
        self.app_module = app_module

    def runTest(self):
        registry.call_hook('before_each', 'app', self.app_module)
        result = self.runner.run()
        registry.call_hook('after_each', 'app', self.app_module, result)
