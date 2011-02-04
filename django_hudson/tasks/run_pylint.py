# -*- coding: utf-8 -*-
# pylint: disable=W0201
import os, sys
from pylint import lint
from pylint.reporters.text import ParseableTextReporter
from django.conf import settings
from django_hudson.tasks import BaseTask

class Task(BaseTask):
    def add_options(self, group):
        group.add_option("--pylint-rcfile",
                dest="pylint_rcfile",
                help="pylint configuration file. Default: %s" % Task.default_config_path())
        group.add_option("--pylint-errors-only",
                dest="pylint_errors_only",
                action="store_true", default=False,
                help="pylint output errors only mode")

    def configure(self, test_labels, options):
        self.test_labels = test_labels
        self.config_path = options['pylint_rcfile'] or Task.default_config_path()
        
        output_dir = options['output_dir'] or ''
        if output_dir:
            self.output = open(os.path.join(output_dir,'pylint.report'), 'w')
        else:
            self.output = sys.stdout

        self.errors_only = options['pylint_errors_only']

    def run_task(self):
        args = ["--rcfile=%s" % self.config_path] 
        if self.errors_only:
            args += ['--errors-only']
        args += list(self.test_labels)

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

