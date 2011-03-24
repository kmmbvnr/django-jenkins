# -*- coding: utf-8 -*-
# pylint: disable=W0201
import os
import sys
from optparse import make_option
from django.conf import settings
from django_jenkins.tasks import BaseTask, get_apps_under_test


if sys.version_info[1] < 5:
    raise AssertionError('pylint task require python>=2.5 version')

from pylint import lint
from pylint.reporters.text import ParseableTextReporter


class Task(BaseTask):
    option_list = [make_option("--pylint-rcfile",
                               dest="pylint_rcfile",
                               help="pylint configuration file"),
                   make_option("--pylint-errors-only",
                               dest="pylint_errors_only",
                               action="store_true", default=False,
                               help="pylint output errors only mode")]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)

        self.test_all = options['test_all']
        self.config_path = options['pylint_rcfile'] or Task.default_config_path()
        self.errors_only = options['pylint_errors_only']

        if options.get('pylint_file_output', True):
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir, 'pylint.report'), 'w')
        else:
            self.output = sys.stdout

    def teardown_test_environment(self, **kwargs):
        args = ["--rcfile=%s" % self.config_path]
        if self.errors_only:
            args += ['--errors-only']
        args += get_apps_under_test(self.test_labels, self.test_all)

        lint.Run(args, reporter=ParseableTextReporter(output=self.output), exit=False)

        return True

    @staticmethod
    def default_config_path():
        rcfile = getattr(settings, 'PYLINT_RCFILE', 'pylint.rc')
        if os.path.exists(rcfile):
            return rcfile

        # use build-in
        root_dir = os.path.normpath(os.path.dirname(__file__))
        return os.path.join(root_dir, 'pylint.rc')
