import os
from optparse import make_option
from django.conf import settings

from pylint import lint
from pylint.reporters.text import TextReporter


class ParseableTextReporter(TextReporter):
    """
    Outputs messages in a form recognized by jenkins

    <filename>:<linenum>:<msg>
    """
    name = 'parseable'
    line_format = '{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}'


class Reporter(object):
    option_list = (
        make_option("--pylint-rcfile",
                    dest="pylint_rcfile",
                    help="pylint configuration file"),
        make_option("--pylint-errors-only",
                    dest="pylint_errors_only",
                    action="store_true", default=False,
                    help="pylint output errors only mode")
    )

    def run(self, apps_locations, **options):
        output = open(os.path.join(options['output_dir'], 'pylint.report'), 'w')

        args = ["--rcfile=%s" % self.get_config_path(options)]
        if options['pylint_errors_only']:
            args += ['--errors-only']
        args += apps_locations

        lint.Run(args, reporter=ParseableTextReporter(output=output), exit=False)

    def get_config_path(self, options):
        if options['pylint_rcfile']:
            return options['pylint_rcfile']

        rcfile = getattr(settings, 'PYLINT_RCFILE', 'pylint.rc')
        if os.path.exists(rcfile):
            return rcfile

        # use build-in
        root_dir = os.path.normpath(os.path.dirname(__file__))
        return os.path.join(root_dir, 'pylint.rc')
