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
    option_list = [make_option("--jshint-interpreter",
                               dest="jshint_interpreter",
                               help="Javascript interpreter for running jshint"),
                   make_option("--jshint-implementation",
                               dest="jshint_implementation",
                               help="Full path to jshint.js, by default used build-in"),
                   make_option("--jshint-with-staticdirs",
                               dest="jshint-with-staticdirs",
                               default=False, action="store_true",
                               help="Check js files located in STATIC_DIRS settings"),
                   make_option("--jshint-with-minjs",
                               dest="jshint_with-minjs",
                               default=False, action="store_true",
                               help="Do not ignore .min.js files"),
                   make_option("--jshint-exclude",
                               dest="jshint_exclude", default="",
                               help="Exclude patterns"),
                   make_option("--jshint-config",
                               dest="jshint_config", default="{ browser: true }",
                               help="JSHINT options see http://www.jshint.com/docs/")]                               

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']
        self.to_file = options.get('jshint_file_output', True)
        self.with_static_dirs = options.get('jshint-with-staticdirs', False)
        self.jshint_with_minjs = options.get('jshint_with-minjs', False)

        root_dir = os.path.normpath(os.path.dirname(__file__))

        self.interpreter = options['jshint_interpreter'] or \
                          getattr(settings, 'JSHINT_INTERPRETER', None)
        if not self.interpreter:
            self.interpreter = find_first_existing_executable(
                [('node', '--help'), ('rhino', '--help')])
            if not self.interpreter:
                raise ValueError('No suitable js interpreter found. Please install nodejs or rhino')

        self.implementation = options['jshint_implementation']
        if not self.implementation:
            self.implementation = os.path.join(root_dir, 'jshint', 'jshint.js')

        if self.to_file:
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = codecs.open(os.path.join(output_dir, 'jshint.xml'), 'w', 'utf-8')
        else:
            self.output = sys.stdout

        self.runner = os.path.join(root_dir, 'jshint_runner.js')
        self.exclude = options['jshint_exclude'].split(',')
        self.config = options['jshint_config']

    def teardown_test_environment(self, **kwargs):
        fmt = 'text'
        if self.to_file:
            fmt = 'xml'

        if self.to_file:
            self.output.write('<?xml version=\"1.0\" encoding=\"utf-8\"?><jslint>')

        for path in self.static_files_iterator():
            jshint_output = check_output(
                [self.interpreter, self.runner, self.implementation, path, fmt, self.config])
            self.output.write(jshint_output.decode('utf-8'))

        if self.to_file:
            self.output.write('</jslint>');

    def static_files_iterator(self):
        locations = get_apps_locations(self.test_labels, self.test_all)

        def in_tested_locations(path):
            if not self.jshint_with_minjs and path.endswith('.min.js'):
                return False

            for location in list(locations):
                if path.startswith(location):
                    return True
            if self.with_static_dirs:
                for location in list(settings.STATICFILES_DIRS):
                    if path.startswith(location):
                        return True
            return False
            
        def is_excluded(path):
            for pattern in self.exclude:
                if fnmatch.fnmatchcase(path, pattern):
                    return True
            return False
        
        if hasattr(settings, 'JSHINT_CHECKED_FILES'):
            for path in settings.JSHINT_CHECKED_FILES:
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
                        path = os.path.join(dirpath, filename)
                        if filename.endswith('.js') and in_tested_locations(path) and not is_excluded(path):
                            yield path

