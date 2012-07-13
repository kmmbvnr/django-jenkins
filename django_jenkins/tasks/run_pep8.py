# -*- coding: utf-8 -*-
import os
import sys
import pep8
from optparse import make_option
from django_jenkins.functions import relpath
from django_jenkins.tasks import BaseTask, get_apps_locations


class Task(BaseTask):

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

    def teardown_test_environment(self, **kwargs):
        locations = get_apps_locations(self.test_labels, self.test_all)

        class JenkinsReport(pep8.BaseReport):
            def error(instance, line_number, offset, text, check):
                code = super(JenkinsReport, instance).error(line_number, offset, text, check)

                if not code:
                    return
                sourceline = instance.line_offset + line_number
                self.output.write('%s:%s:%s: %s\n' % (instance.filename, sourceline, offset+1, text))


        pep8style = pep8.StyleGuide(parse_argv=False, config_file='.pep8', reporter=JenkinsReport)

        for location in locations:
            pep8style.input_dir(relpath(location))

        self.output.close()
