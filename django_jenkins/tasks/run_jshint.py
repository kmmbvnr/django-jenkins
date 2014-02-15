# -*- coding: utf-8 -*-
import os
import sys
import codecs
import fnmatch
import subprocess
from optparse import make_option
from django.conf import settings
from django_jenkins.functions import CalledProcessError
from django_jenkins.tasks import BaseTask, get_apps_locations


class Task(BaseTask):
    option_list = [
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
        make_option("--jshint-static-dirname",
                    dest="jshint_static-dirname", default="static",
                    help="Name of dir with js static files")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']
        self.to_file = options.get('jshint_file_output', True)
        self.with_static_dirs = options.get('jshint-with-staticdirs', False)
        self.jshint_with_minjs = options.get('jshint_with-minjs', False)

        if self.to_file:
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = codecs.open(os.path.join(output_dir, 'jshint.xml'), 'w', 'utf-8')
        else:
            self.output = sys.stdout

        self.exclude = options['jshint_exclude'].split(',')
        self.static_dirname = options.get('jshint_static-dirname', 'static')

    def teardown_test_environment(self, **kwargs):
        files = [path for path in self.static_files_iterator()]

        cmd = ['jshint']
        if self.to_file:
            cmd += ['--jslint-reporter']
        cmd += files

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, err = process.communicate()
        retcode = process.poll()
        if retcode not in [0, 1, 2]:  # normal jshint return codes
            raise CalledProcessError(retcode, cmd, output='%s\n%s' % (output, err))

        self.output.write(output.decode('utf-8'))
        self.output.close()

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
                for dirpath, dirnames, filenames in os.walk(os.path.join(location, self.static_dirname)):
                    for filename in filenames:
                        path = os.path.join(dirpath, filename)
                        if filename.endswith('.js') and in_tested_locations(path) and not is_excluded(path):
                            yield path
