# -*- coding: utf-8; mode: django -*-
import os
import sys
from optparse import make_option
from django.conf import settings
from django_jenkins.functions import check_output, relpath
from django_jenkins.tasks import BaseTask, get_apps_locations


class Task(BaseTask):
    option_list = [make_option("--csslint-interpreter",
                               dest="csslint_interpreter",
                               help="Javascript interpreter for running csslint"),
                   make_option("--csslint-implementation",
                               dest="csslint_implementation",
                               help="Full path to csslint-IMPL.js, by default used build-in"),
                   make_option("--csslint-exclude",
                               dest="csslint_exclude", default="",
                               help="Exclude patterns")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']
        self.to_file = options.get('csslint_file_output', True)
        root_dir = os.path.normpath(os.path.dirname(__file__))

        self.intepreter = options['csslint_interpreter'] or \
                          getattr(settings, 'CSSLINT_INTERPRETER', 'rhino')

        self.implementation = options['csslint_implementation']
        if not self.implementation:
            self.implementation = os.path.join(root_dir, 'csslint', 'release', 'csslint-rhino.js')

        if self.to_file:
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir, 'csslint.report'), 'w')
        else:
            self.output = sys.stdout

        self.exclude = options['csslint_exclude']

    def teardown_test_environment(self, **kwargs):
        files = [relpath(path) for path in self.static_files_iterator()]
        if self.to_file:
            fmt = 'lint-xml'
        else:
            fmt = 'text'

        csslint_output = check_output([self.intepreter, self.implementation, '--format=%s' % fmt] + files)
        self.output.write(csslint_output)

    def static_files_iterator(self):
        locations = get_apps_locations(self.test_labels, self.test_all)

        def in_tested_locations(path):
            for location in locations:
                if path.startswith(location):
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
                for dirpath, dirnames, filenames in os.walk(os.path.join(location, 'static')):
                    for filename in filenames:
                        if filename.endswith('.css') and in_tested_locations(os.path.join(dirpath, filename)):
                            yield os.path.join(dirpath, filename)

