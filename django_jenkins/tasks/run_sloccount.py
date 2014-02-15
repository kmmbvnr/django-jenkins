# -*- coding: utf-8 -*-
import os
import sys
from optparse import make_option
from django_jenkins.functions import check_output
from django_jenkins.tasks import BaseTask, get_apps_locations


class Task(BaseTask):
    option_list = [
        make_option("--sloccount-with-migrations",
                    action="store_true", default=False,
                    dest="sloccount_with_migrations",
                    help="Count migrations sloc.")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']
        self.with_migrations = options['sloccount_with_migrations']

        if options.get('sloccount_file_output', True):
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir,
                                            'sloccount.report'), 'w')
        else:
            self.output = sys.stdout

    def teardown_test_environment(self, **kwargs):
        locations = get_apps_locations(self.test_labels, self.test_all)

        report_output = check_output(
            ['sloccount', "--duplicates", "--wide", "--details"] + locations)
        report_output = report_output.decode('utf-8')

        if self.with_migrations:
            self.output.write(report_output)
        else:
            for line in report_output.splitlines():
                if (os.sep + 'migrations' + os.sep) in line:
                    continue
                self.output.write(line)
                self.output.write('\n')
        self.output.close()
