# -*- coding: utf-8 -*-
import re, os, pep8, sys
from optparse import make_option
from django_jenkins.tasks import BaseTask, get_apps_under_test
from django.db.models import get_app

def relpath(path, start=os.path.curdir):
    """Return a relative version of a path"""

    if not path:
        raise ValueError("no path specified")

    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)

    # Work out how much of the filepath is shared by start and path.
    i = len(os.path.commonprefix([start_list, path_list]))

    rel_list = [os.path.pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return os.path.curdir
    return os.path.join(*rel_list)


class Task(BaseTask):
    option_list = [make_option("--pep8-exclude",
                               dest="pep8-exclude", default=pep8.DEFAULT_EXCLUDE,
                               help="exclude files or directories which match these "
                               "comma separated patterns (default: %s)" %
                               pep8.DEFAULT_EXCLUDE),
                   make_option("--pep8-select", dest="pep8-select",
                               help="select errors and warnings (e.g. E,W6)"),
                   make_option("--pep8-ignore", dest="pep8-ignore",
                               help="skip errors and warnings (e.g. E4,W)")]
    
    def __init__(self, test_labels, options):
        super(Task, self).__init__(test_labels, options)
        self.test_all = options['test_all']

        if options.get('pep8_file_output', True):
            output_dir = options['output_dir']
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.output = open(os.path.join(output_dir, 'pep8.report'), 'w')
        else:
            self.output = sys.stdout

        self.pep8_options = ['--exclude=%s' % options['pep8-exclude']]
        if options['pep8-select']:
            self.pep8_options.append('--select=%s' % options['pep8-select'])
        if options['pep8-exclude']:
            self.pep8_options.append('--exclude=%s' % options['pep8-exclude'])

    def teardown_test_environment(self, **kwargs):
        locations = [os.path.dirname(get_app(app_name.split('.')[-1]).__file__) \
                     for app_name in get_apps_under_test(self.test_labels, self.test_all)]
        pep8.process_options(self.pep8_options + locations)

        # run pep8 tool with captured output
        def report_error(instance, line_number, offset, text, check):
            filepath = relpath(instance.filename)
            message = re.sub(r'([WE]\d+)', r'[\1] PEP8:', text)
            sourceline = instance.line_offset + line_number
            self.output.write('%s:%s: %s\n' % (filepath, sourceline, message))
        pep8.Checker.report_error = report_error

        for location in locations:
            pep8.input_dir(location, runner=pep8.input_file)

        self.output.close()

