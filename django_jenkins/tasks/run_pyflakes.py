# -*- coding: utf-8 -*-
import os
import re
import sys
from optparse import make_option
from pyflakes.scripts import pyflakes
from cStringIO import StringIO
from django_jenkins.functions import relpath
from django_jenkins.tasks import BaseTask, get_apps_locations


class Task(BaseTask):
    option_list = [
        make_option("--pyflakes-with-migrations",
                    action="store_true", default=False,
                    dest="pyflakes_with_migrations",
                    help="Don't check migrations with pyflakes.")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']
        self.with_migrations = options['pyflakes_with_migrations']

        if options.get('pyflakes_file_output', True):
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir, 'pyflakes.report'), 'w')
        else:
            self.output = sys.stdout

    def teardown_test_environment(self, **kwargs):
        locations = get_apps_locations(self.test_labels, self.test_all)

        # run pyflakes tool with captured output
        old_stdout, pyflakes_output = sys.stdout, StringIO()
        sys.stdout = pyflakes_output
        try:
            for location in locations:
                if os.path.isdir(location):
                    for dirpath, dirnames, filenames in os.walk(relpath(location)):
                        if not self.with_migrations and 'migrations' in dirpath:
                            continue
                        for filename in filenames:
                            if filename.endswith('.py'):
                                pyflakes.checkPath(os.path.join(dirpath, filename))
                else:
                    pyflakes.checkPath(relpath(location))
        finally:
            sys.stdout = old_stdout

        # save report
        pyflakes_output.reset()
        while True:
            line = pyflakes_output.readline()
            if not line:
                break
            message = re.sub(r': ', r': [E] PYFLAKES:', line)
            self.output.write(message)

        self.output.close()
