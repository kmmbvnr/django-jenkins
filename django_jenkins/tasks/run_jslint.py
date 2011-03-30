# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from optparse import make_option
from django.conf import settings
from django_jenkins.tasks import BaseTask

class Task(BaseTask):
    option_list = [make_option("--jslint-interpreter",
                               dest="jslint_interpreter",
                               help="Javascript interpreter for running jslint"),
                   make_option("--jslint-implementation",
                               dest="jslint_implementation",
                               help="Full path to fulljslint.js, by default used build-in")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)

        root_dir = os.path.normpath(os.path.dirname(__file__))

        self.intepreter = options['jslint_interpreter'] or \
                          getattr(settings, 'JSLINT_INTERPRETER', 'rhino')

        self.implementation = options['jslint_implementation']
        if not self.implementation:
            self.implementation = os.path.join(root_dir, 'jslint', 'fulljslint.js')

        if options.get('jslint_file_output', True):
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir, 'jslint.report'), 'w')
        else:
            self.output = sys.stdout

        self.runner = os.path.join(root_dir, 'jslint_runner.js')

    def teardown_test_environment(self, **kwargs):
        for path in self.static_files_iterator():
            jslint_output = subprocess.check_output(
                [self.intepreter, self.runner, self.implementation, path])
            self.output.write(jslint_output)
        print jslint_output

    def static_files_iterator(self):
        if hasattr(settings, 'JSLINT_CHECKED_FILES'):
            for path in settings.JSLINT_CHECKED_FILES:
                yield path
        elif 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
            # use django.contrib.staticfiles
            from django.contrib.staticfiles import finders

            for finder in finders.get_finders():
                for path, _ in finder.list(self.exclude):
                    yield path
        else:
            # TODO scan apps directories for static folders
            pass


