# -*- coding: utf-8 -*-
import os
import sys
from optparse import make_option
from django.conf import settings
from django_jenkins.functions import check_output, relpath, find_first_existing_executable
from django_jenkins.tasks import BaseTask, get_apps_locations

class Task(BaseTask):
    option_list = [make_option("--jslint-interpreter",
                               dest="jslint_interpreter",
                               help="Javascript interpreter for running jslint"),
                   make_option("--jslint-implementation",
                               dest="jslint_implementation",
                               help="Full path to jslint.js, by default used build-in"),
                   make_option("--jslint-with-staticdirs",
                               dest="jslint-with-staticdirs",
                               default=False, action="store_true",
                               help="Check js files located in STATIC_DIRS settings"),
                   make_option("--jslint-with-minjs",
                               dest="jslint_with-minjs",
                               default=False, action="store_true",
                               help="Do not ignore .min.js files"),
                   make_option("--jslint-exclude",
                               dest="jslint_exclude", default="",
                               help="Exclude patterns")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']
        self.to_file = options.get('jslint_file_output', True)
        self.with_static_dirs = options.get('jslint-with-staticdirs', False)
        self.jslint_with_minjs = options.get('jslint_with-minjs', False)

        root_dir = os.path.normpath(os.path.dirname(__file__))

        self.interpreter = options['jslint_interpreter'] or \
                          getattr(settings, 'JSLINT_INTERPRETER', None)
        if not self.interpreter:
            self.interpreter = find_first_existing_executable(
                [('node', '--help'), ('rhino', '--help')])
            if not self.interpreter:
                raise ValueError('No suitable js interpreter found. Please install nodejs or rhino')

        self.implementation = options['jslint_implementation']
        if not self.implementation:
            self.implementation = os.path.join(root_dir, 'jslint', 'jslint.js')

        if self.to_file:
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir, 'jslint.xml'), 'w')
        else:
            self.output = sys.stdout

        self.runner = os.path.join(root_dir, 'jslint_runner.js')
        self.exclude = options['jslint_exclude'].split(',')

    def teardown_test_environment(self, **kwargs):
        fmt = 'text'
        if self.to_file:
            fmt = 'xml'

        if self.to_file:
            self.output.write('<?xml version=\"1.0\" encoding=\"utf-8\"?><jslint>')

        for path in self.static_files_iterator():
            jslint_output = check_output(
                [self.interpreter, self.runner, self.implementation, relpath(path), fmt])
            self.output.write(jslint_output)

        if self.to_file:
            self.output.write('</jslint>');

    def static_files_iterator(self):
        locations = get_apps_locations(self.test_labels, self.test_all)

        def in_tested_locations(path):
            if not self.jslint_with_minjs and path.endswith('.min.js'):
                return False

            for location in list(locations):
                if path.startswith(location):
                    return True
            if self.with_static_dirs:
                for location in list(settings.STATICFILES_DIRS):
                    if path.startswith(location):
                        return True
            return False
        
        if hasattr(settings, 'JSLINT_CHECKED_FILES'):
            for path in settings.JSLINT_CHECKED_FILES:
                yield path

        if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
            # use django.contrib.staticfiles
            from django.contrib.staticfiles import finders

            for finder in finders.get_finders():
                for path, storage in finder.list(self.exclude):
                    path = os.path.join(storage.location, path)                
                    if path.endswith('.js') and in_tested_locations(path):
                        yield path
        else:
            # scan apps directories for static folders
            for location in locations:
                for dirpath, dirnames, filenames in os.walk(os.path.join(location, 'static')):
                    for filename in filenames:
                        if filename.endswith('.js') and in_tested_locations(os.path.join(dirpath, filename)):
                            yield os.path.join(dirpath, filename)

