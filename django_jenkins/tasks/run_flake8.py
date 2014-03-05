import os
import sys
import pep8

from flake8.engine import get_style_guide
from django_jenkins.tasks import get_apps_locations
from django_jenkins.tasks.run_pep8 import Task
from django_jenkins.functions import relpath
from optparse import make_option


class Task(Task):
    """
    Runs flake8 on python files.
    """
    option_list = [
        make_option('--max-complexity',
                    dest='max_complexity',
                    default='-1',
                    help='McCabe complexity treshold'),
        make_option("--pep8-exclude",
                    dest="pep8-exclude",
                    default=pep8.DEFAULT_EXCLUDE + ",migrations",
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
                    help="PEP8 configuration file"),
    ]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']

        self.max_complexity = int(options['max_complexity'])

        if options.get('flake8_file_output', True):
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir, 'flake8.report'), 'w')
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
                self.output.write('%s:%s:%s: %s\n' % (instance.filename, sourceline, offset + 1, text))

        pep8style = get_style_guide(parse_argv=False, config_file=self.pep8_rcfile,
                                    reporter=JenkinsReport, max_complexity=self.max_complexity,
                                    **self.pep8_options)

        for location in locations:
            pep8style.input_dir(relpath(location))

        self.output.close()
