# -*- coding: utf-8; mode: django -*-
import os
import subprocess
import sys
import fnmatch
import codecs
from optparse import make_option
from django.conf import settings
from django_jenkins.functions import (CalledProcessError,
                                      find_first_existing_executable)
from django_jenkins.tasks import BaseTask, get_apps_locations


class Task(BaseTask):
    option_list = [
       make_option("--csslint-interpreter",
                   dest="csslint_interpreter",
              help="Javascript interpreter for running csslint"),
       make_option("--csslint-implementation",
                   dest="csslint_implementation",
              help="Full path to csslint-IMPL.js, by default used build-in"),
       make_option("--csslint-with-staticdirs",
                   dest="csslint_with-staticdirs",
                   default=False, action="store_true",
              help="Check css files located in STATIC_DIRS settings"),
       make_option("--csslint-with-mincss",
                   dest="csslint_with_mincss",
                   default=False, action="store_true",
                   help="Do not ignore .min.css files"),
       make_option("--csslint-exclude",
                   dest="csslint_exclude", default="",
              help="Exclude patterns")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']
        self.to_file = options.get('csslint_file_output', True)
        self.with_static_dirs = options.get('csslint_with-staticdirs', False)
        self.csslint_with_minjs = options.get('csslint_with_mincss', False)
        root_dir = os.path.normpath(os.path.dirname(__file__))

        self.interpreter = options['csslint_interpreter'] or \
                          getattr(settings, 'CSSLINT_INTERPRETER', None)
        if not self.interpreter:
            self.interpreter = find_first_existing_executable(
                [('node', '--help'), ('rhino', '--help')])
            if not self.interpreter:
                raise ValueError('No sutable js interpreter found. '
                                 'Please install nodejs or rhino')

        self.implementation = options['csslint_implementation']
        if not self.implementation:
            runner = os.path.basename(self.interpreter)
            if 'rhino' in runner:
                self.implementation = os.path.join(root_dir, 'csslint',
                                                 'release', 'csslint-rhino.js')
            elif 'node' in runner:
                self.implementation = os.path.join(root_dir, 'csslint',
                                                    'release', 'npm', 'cli.js')
            else:
                raise ValueError('No sutable css lint runner found for %s'
                                                            % self.interpreter)

        if self.to_file:
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = codecs.open(os.path.join(output_dir, 'csslint.report'), 'w', 'utf-8')
        else:
            self.output = sys.stdout

        self.exclude = options['csslint_exclude'].split(',')

    def teardown_test_environment(self, **kwargs):
        files = [path for path in self.static_files_iterator()]
        if self.to_file:
            fmt = 'lint-xml'
        else:
            fmt = 'text'

        if files:
            cmd = [self.interpreter,
                   self.implementation, '--format=%s' % fmt] + files

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output, err = process.communicate()
            retcode = process.poll()
            if retcode not in [0, 1]:  # normal csslint return codes
                raise CalledProcessError(retcode, cmd,
                                         output=output + '\n' + err)

            self.output.write(output.decode('utf-8'))
        elif self.to_file:
            self.output.write('<?xml version="1.0" encoding='
                              '"utf-8"?><lint></lint>')

    def static_files_iterator(self):
        locations = get_apps_locations(self.test_labels, self.test_all)

        def in_tested_locations(path):
            if not self.csslint_with_minjs and path.endswith('.min.css'):
                return False

            for location in locations:
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

        if hasattr(settings, 'CSSLINT_CHECKED_FILES'):
            for path in settings.CSSLINT_CHECKED_FILES:
                yield path

        if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
            # use django.contrib.staticfiles
            from django.contrib.staticfiles import finders

            for finder in finders.get_finders():
                for path, storage in finder.list(self.exclude):
                    path = os.path.join(storage.location, path)
                    if path.endswith('.css') and in_tested_locations(path):
                        yield path
        else:
            # scan apps directories for static folders
            for location in locations:
                for dirpath, dirnames, filenames in \
                                os.walk(os.path.join(location, 'static')):
                    for filename in filenames:
                        path = os.path.join(dirpath, filename)
                        if filename.endswith('.css') and \
                             in_tested_locations(path) and not \
                                 is_excluded(path):
                            yield path
