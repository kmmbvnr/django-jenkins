import os
import pep8

from flake8.engine import get_style_guide
from django.conf import settings
from optparse import make_option
import ConfigParser
from ConfigParser import NoOptionError


class Reporter(object):
    """
    Runs flake8 on python files.
    """
    option_list = (
        make_option('--max-complexity',
                    dest='max_complexity',
                    default=None,
                    help='McCabe complexity treshold'),
        make_option("--pep8-exclude",
                    dest="pep8-exclude",
                    default=None,
                    help="exclude files or directories which match these "
                    "comma separated patterns (default: %s)" %
                    (pep8.DEFAULT_EXCLUDE + ",south_migrations")),
        make_option("--pep8-select", dest="pep8-select",
                    help="select errors and warnings (e.g. E,W6)"),
        make_option("--pep8-ignore", dest="pep8-ignore",
                    help="skip errors and warnings (e.g. E4,W)"),
        make_option("--pep8-max-line-length",
                    dest="pep8-max-line-length", type='int',
                    help="set maximum allowed line length (default: %d)" %
                    pep8.MAX_LINE_LENGTH),
        make_option("--pep8-rcfile", dest="pep8-rcfile",
                    help="PEP8 configuration file"),
    )

    def run(self, apps_locations, **options):
        output = open(os.path.join(options['output_dir'], 'flake8.report'), 'w')

        class JenkinsReport(pep8.BaseReport):
            def error(instance, line_number, offset, text, check):
                code = super(JenkinsReport, instance).error(line_number, offset, text, check)

                if not code:
                    return
                sourceline = instance.line_offset + line_number
                output.write('%s:%s:%s: %s\n' % (instance.filename, sourceline, offset + 1, text))

        pep8_options = {'config_file': self.get_config_path(options)}

        max_complexity = None

        if options['max_complexity'] is None:
            if pep8_options['config_file']:
                max_complexity = self.get_max_complexity_from_config(
                    pep8_options['config_file'])
        else:
            max_complexity = int(options['max_complexity'])

        if options['pep8-exclude'] is None:
            if pep8_options['config_file'] is None:
                pep8_options = {'exclude': (pep8.DEFAULT_EXCLUDE + ",south_migrations").split(',')}
        else:
            pep8_options = {'exclude': options['pep8-exclude'].split(',')}

        if options['pep8-select']:
            pep8_options['select'] = options['pep8-select'].split(',')
        if options['pep8-ignore']:
            pep8_options['ignore'] = options['pep8-ignore'].split(',')
        if options['pep8-max-line-length']:
            pep8_options['max_line_length'] = options['pep8-max-line-length']

        pep8style = get_style_guide(
            parse_argv=False,
            reporter=JenkinsReport,
            max_complexity=max_complexity,
            jobs='1',
            **pep8_options)

        pep8style.options.report.start()
        for location in apps_locations:
            pep8style.input_dir(os.path.relpath(location))
        pep8style.options.report.stop()

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

    def get_max_complexity_from_config(self, config):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config)
        try:
            return config_parser.getint('flake8', 'max-complexity')
        except NoOptionError:
            return None
