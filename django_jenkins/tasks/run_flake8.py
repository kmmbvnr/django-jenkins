import os
import sys

from io import BytesIO

# Use pep8 from flake8 to avoid weird errors resulting from
# version mismatch.
from flake8 import pep8

from django_jenkins.tasks import (
    BaseTask,
    get_apps_locations
)
from django_jenkins.functions import relpath

from optparse import make_option


class Task(BaseTask):
    """
    Runs flake8 on python files.
    """
    option_list = [
        make_option(
            '--max-complexity',
            dest='max_complexity',
            default='-1',
            help='McCabe complexity treshold'
        ),
    ]

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']

        self.max_complexity = int(options['max_complexity'])

        if options.get('flake8_file_output', True):

            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            self.output = open(
                os.path.join(
                    output_dir,
                    'flake8.report'
                ),
                'w'
            )
        else:
            self.output = sys.stdout

    def teardown_test_environment(self, **kwargs):
        # Local import to avoid intallation errors.
        import flake8.run

        locations = get_apps_locations(
            self.test_labels,
            self.test_all
        )

        paths = flake8.run._get_python_files(locations)
        flake8.run.pep8style = pep8.StyleGuide(
            parse_argv=False,
            config_file=False
        )
        old_stdout, flake8_output = sys.stdout, BytesIO()
        sys.stdout = flake8_output
        warnings = 0
        for path in paths:
            # We could pass ignore paths
            # but I need to figure out first how to do it
            warnings += flake8.run.check_file(
                path,
                complexity=self.max_complexity
            )

        sys.stdout = old_stdout

        flake8_output.seek(0)

        while True:
            line = flake8_output.readline()
            if not line:
                break

            # Make sure the path is relative in the report
            bits = line.split(':')
            bits[0] = relpath(bits[0])
            self.output.write(':'.join(bits))

        self.output.close()
