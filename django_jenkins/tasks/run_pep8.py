# -*- coding: utf-8 -*-
import re
import os
import sys
import pep8
from optparse import make_option
from django_jenkins.functions import relpath
from django_jenkins.tasks import BaseTask, get_apps_locations


class Task(BaseTask):
    option_list = [make_option("--pep8-exclude",
                               dest="pep8-exclude", default=pep8.DEFAULT_EXCLUDE + ",migrations",
                               help="exclude files or directories which match these "
                               "comma separated patterns (default: %s)" %
                               pep8.DEFAULT_EXCLUDE),
                   make_option("--pep8-select", dest="pep8-select",
                               help="select errors and warnings (e.g. E,W6)"),
                   make_option("--pep8-ignore", dest="pep8-ignore",
                               help="skip errors and warnings (e.g. E4,W)")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']

        if options.get('pep8_file_output', True):
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir, 'pep8.report'), 'w')
        else:
            self.output = sys.stdout

        self.pep8_options = ['--exclude=%s' % options['pep8-exclude']]
        if options['pep8-select']:
            self.pep8_options.append('--select=%s' % options['pep8-select'])
        if options['pep8-ignore']:
            self.pep8_options.append('--ignore=%s' % options['pep8-ignore'])

    def teardown_test_environment(self, **kwargs):
        locations = get_apps_locations(self.test_labels, self.test_all)
        pep8.process_options(self.pep8_options + locations)

        # run pep8 tool with captured output
        def report_error(instance, line_number, offset, text, check):
            code = text[:4]
            if pep8.ignore_code(code):
                return
            sourceline = instance.line_offset + line_number
            self.output.write('%s:%s:%s: %s\n' % (instance.filename, sourceline, offset+1, text))
        pep8.Checker.report_error = report_error

        for location in locations:
            pep8.input_dir(relpath(location), runner=pep8.input_file)

        self.output.close()
