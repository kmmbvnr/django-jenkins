# -*- coding: utf-8 -*-
import os
import sys
import codecs
from django_jenkins.functions import check_output
from django_jenkins.tasks import BaseTask, get_apps_locations


class PushDir:
    def __init__(self, newPath):
        self.pushedPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.pushedPath)

    def __exit__(self, error, value, traceback):
        os.chdir(self.savedPath)


class Task(BaseTask):
    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']
        self.to_files = options.get('testem_file_output', True)

        if self.to_files:
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output_dir = os.path.abspath(output_dir)

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
            sys.stdout.write('Executing: %s\n' % test)
            app_dir = os.path.dirname(os.path.dirname(test))
            manage_dir = os.path.abspath(os.path.join(app_dir, '..'))
            with PushDir(manage_dir):
                testem_output = check_output(
                    ['testem', 'ci', '-f', test])
                if self.to_files:
                    app_name = os.path.basename(app_dir)
                    output = codecs.open(os.path.join(self.output_dir, "testem-%s.tap" % app_name), 'w', 'utf-8')
                else:
                    output = sys.stdout
                output.write(testem_output.decode('utf-8'))
