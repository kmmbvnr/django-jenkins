import os
import sys

# Use pep8 from flake8 to avoid weird errors resulting from
# version mismatch.
from flake8 import pep8

from django_jenkins.tasks import (
    BaseTask,
    get_apps_locations
)
from django_jenkins.functions import relpath

from StringIO import StringIO


class Task(BaseTask):
    """
    Runs flake8 on python files.
    """

    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']
        output_dir = options['output_dir']
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # We always write to a file. Can't think of a scenario
        # when jenkins would want to write the report to stdout.
        self.output = open(
            os.path.join(
                output_dir,
                'flake8.report'
            ),
            'w'
        )

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
        old_stdout, flake8_output = sys.stdout, StringIO()
        sys.stdout = flake8_output
        warnings = 0
        for path in paths:
            # We could pass ignore paths and max complexity there,
            # but I need to figure out first how to do it
            warnings += flake8.run.check_file(path)

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
