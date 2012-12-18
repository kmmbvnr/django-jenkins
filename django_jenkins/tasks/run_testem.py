# -*- coding: utf-8 -*-
import os
import sys
from django_jenkins.functions import check_output
from django_jenkins.tasks import BaseTask, get_apps_locations


class Task(BaseTask):

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.output = sys.stdout
        self.test_all = options['test_all']

    def test_files_iterator(self):
        locations = get_apps_locations(self.test_labels, self.test_all)

        def in_tested_locations(path):
            for location in list(locations):
                if path.startswith(location):
                    return True
            return False

         # scan apps directories for static folders
        for location in locations:
            for dirpath, dirnames, filenames in os.walk(os.path.join(location, 'testem')):
                for filename in filenames:
                    path = os.path.join(dirpath, filename)
                    if filename.endswith('.yml') and in_tested_locations(path):
                        yield path

    def teardown_test_environment(self, **kwargs):

        for test in self.test_files_iterator():
            self.output.write('Executing: %s' % test)
            testem_output = check_output(
                ['testem', 'ci', '-f', test])
            self.output.write(testem_output.decode('utf-8'))
            self.output.write('*********')
