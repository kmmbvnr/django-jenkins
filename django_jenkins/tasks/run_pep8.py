import os.path
import pep8
from optparse import make_option
from django.conf import settings


class Reporter(object):
    option_list = (
        make_option("--pep8-exclude",
                    dest="pep8-exclude",
                    default=pep8.DEFAULT_EXCLUDE + ",south_migrations",
                    help="exclude files or directories which match these "
                    "comma separated patterns (default: %s)" %
                    pep8.DEFAULT_EXCLUDE),
        make_option("--pep8-select", dest="pep8-select",
                    help="select errors and warnings (e.g. E,W6)"),
        make_option("--pep8-ignore", dest="pep8-ignore",
                    help="skip errors and warnings (e.g. E4,W)"),
        make_option("--pep8-max-line-length",
                    dest="pep8-max-line-length", type='int',
                    help="set maximum allowed line length (default: %d)" %
                    pep8.MAX_LINE_LENGTH),
        make_option("--pep8-rcfile", dest="pep8-rcfile",
                    help="PEP8 configuration file")
    )

    def run(self, apps_locations, **options):
        output = open(os.path.join(options['output_dir'], 'pep8.report'), 'w')

        class JenkinsReport(pep8.BaseReport):
            def error(instance, line_number, offset, text, check):
                code = super(JenkinsReport, instance).error(line_number, offset, text, check)
                if code:
                    sourceline = instance.line_offset + line_number
                    output.write('%s:%s:%s: %s\n' % (instance.filename, sourceline, offset + 1, text))

        pep8_options = {'exclude': options['pep8-exclude'].split(',')}
        if options['pep8-select']:
            pep8_options['select'] = options['pep8-select'].split(',')
        if options['pep8-ignore']:
            pep8_options['ignore'] = options['pep8-ignore'].split(',')
        if options['pep8-max-line-length']:
            pep8_options['max_line_length'] = options['pep8-max-line-length']

        pep8style = pep8.StyleGuide(
            parse_argv=False,
            config_file=self.get_config_path(options),
            reporter=JenkinsReport,
            **pep8_options)

        pep8style.options.report.start()
        for location in apps_locations:
            pep8style.input_dir(os.path.relpath(location))
        pep8style.options.report.stop()

    def get_config_path(self, options):
        if options['pep8-rcfile']:
            return options['pep8-rcfile']

        rcfile = getattr(settings, 'PEP8_RCFILE', 'pep8.rc')
        return rcfile if os.path.exists(rcfile) else None
