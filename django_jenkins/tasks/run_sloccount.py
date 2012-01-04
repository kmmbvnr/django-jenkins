# -*- coding: utf-8 -*-
import os
import sys
from optparse import make_option
from django.conf import settings
from django_jenkins.functions import check_output, relpath
from django_jenkins.tasks import BaseTask, get_apps_locations

class Task(BaseTask):
    option_list = []

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.locations = get_apps_locations(self.test_labels, options['test_all'])   
        if options.get('sloccount_file_output', True):
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir, 'sloccount.report'), 'w')
        else:
            self.output = sys.stdout 
        self.root_dir = os.path.normpath(os.path.dirname(__file__))
        
                                  
    def teardown_test_environment(self, **kwargs):
        report_output = check_output(
            ['sloccount', "--wide", "--details"] + self.locations)
        self.output.write(report_output)
