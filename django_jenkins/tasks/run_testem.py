# -*- coding: utf-8 -*-
import os
import sys
import codecs
import fnmatch
from optparse import make_option
from django.conf import settings
from django_jenkins.functions import check_output, find_first_existing_executable
from django_jenkins.tasks import BaseTask, get_apps_locations

class Task(BaseTask):

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)

        root_dir = os.path.normpath(os.path.dirname(__file__))

        self.config = 'ci'
        self.tests = options['testem_tests']

    def teardown_test_environment(self, **kwargs):

        for test in self.tests:
            testem_output = check_output(
                ['testem', self.config, test])
            self.output.write(testem.decode('utf-8'))

        if self.to_file:
            self.output.write('</testem>');