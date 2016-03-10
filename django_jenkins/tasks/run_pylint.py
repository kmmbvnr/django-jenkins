import os

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
    def add_arguments(self, parser):
        parser.add_argument("--pylint-rcfile",
                            dest="pylint_rcfile",
                            help="pylint configuration file")
        parser.add_argument("--pylint-errors-only",
                            dest="pylint_errors_only",
                            action="store_true", default=False,
                            help="pylint output errors only mode")
        parser.add_argument("--pylint-load-plugins",
                            dest="pylint_load_plugins",
                            help="list of pylint plugins to load")

    def run(self, apps_locations, **options):
        output = open(os.path.join(options['output_dir'], 'pylint.report'), 'w')

        args = []
        args.append("--rcfile=%s" % self.get_config_path(options))
        if self.get_plugins(options):
            args.append('--load-plugins=%s' % self.get_plugins(options))

        if options['pylint_errors_only']:
            args += ['--errors-only']
        args += apps_locations

        lint.Run(args, reporter=ParseableTextReporter(output=output), exit=False)

        output.close()

    def get_plugins(self, options):
        if options.get('pylint_load_plugins', None):
            return options['pylint_load_plugins']

        plugins = getattr(settings, 'PYLINT_LOAD_PLUGIN', None)
        if plugins:
            return ','.join(plugins)

        return None

    def get_config_path(self, options):
        if options['pylint_rcfile']:
            return options['pylint_rcfile']

        rcfile = getattr(settings, 'PYLINT_RCFILE', 'pylint.rc')
        if os.path.exists(rcfile):
            return rcfile

        # use built-in
        root_dir = os.path.normpath(os.path.dirname(__file__))
        return os.path.join(root_dir, 'pylint.rc')
