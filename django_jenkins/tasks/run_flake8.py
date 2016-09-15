import os
import pep8
import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


from flake8.api.legacy import get_style_guide  # Quck hack again, 3d time flake8 would be removed, if no volounters found
from django.conf import settings

from . import set_option


class Reporter(object):
    """
    Runs flake8 on python files.
    """
    def add_arguments(self, parser):
        parser.add_argument('--max-complexity',
                            dest='flake8-max-complexity',
                            type=int,
                            help='McCabe complexity treshold')
        parser.add_argument("--pep8-exclude",
                            dest="pep8-exclude",
                            help="exclude files or directories which match these "
                            "comma separated patterns (default: %s)" %
                            (pep8.DEFAULT_EXCLUDE + ",south_migrations"))
        parser.add_argument("--pep8-select", dest="pep8-select",
                            help="select errors and warnings (e.g. E,W6)")
        parser.add_argument("--pep8-ignore", dest="pep8-ignore",
                            help="skip errors and warnings (e.g. E4,W)")
        parser.add_argument("--pep8-max-line-length",
                            dest="pep8-max-line-length", type=int,
                            help="set maximum allowed line length (default: %d)" %
                            pep8.MAX_LINE_LENGTH)
        parser.add_argument("--pep8-rcfile", dest="pep8-rcfile",
                            help="PEP8 configuration file")

    def run(self, apps_locations, **options):
        output = open(os.path.join(options['output_dir'], 'flake8.report'), 'w')

        pep8_options = {}

        config_file = self.get_config_path(options)
        if config_file is not None:
            pep8_options['config_file'] = config_file

        set_option(pep8_options, 'exclude', options['pep8-exclude'], config_file,
                   default=pep8.DEFAULT_EXCLUDE + ",south_migrations", split=',')

        set_option(pep8_options, 'select', options['pep8-select'], config_file, split=',')

        set_option(pep8_options, 'ignore', options['pep8-ignore'], config_file, split=',')

        set_option(pep8_options, 'max_line_length', options['pep8-max-line-length'], config_file,
                   default=pep8.MAX_LINE_LENGTH)

        set_option(pep8_options, 'max_complexity', options['flake8-max-complexity'], config_file,
                   default=-1)

        old_stdout, flake8_output = sys.stdout, StringIO()
        sys.stdout = flake8_output

        pep8style = get_style_guide(
            parse_argv=False,
            jobs='1',
            **pep8_options)

        try:
            for location in apps_locations:
                pep8style.input_file(os.path.relpath(location))
        finally:
            sys.stdout = old_stdout

        flake8_output.seek(0)
        output.write(flake8_output.read())
        output.close()

    def get_config_path(self, options):
        if options['pep8-rcfile']:
            return options['pep8-rcfile']

        rcfile = getattr(settings, 'PEP8_RCFILE', None)
        if rcfile:
            return rcfile

        if os.path.exists('tox.ini'):
            return 'tox.ini'

        if os.path.exists('setup.cfg'):
            return 'setup.cfg'
