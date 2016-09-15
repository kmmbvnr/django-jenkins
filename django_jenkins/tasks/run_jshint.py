# -*- coding: utf-8 -*-
import os
import codecs
import subprocess

from django.conf import settings
from django_jenkins.tasks import static_files_iterator


class Reporter(object):
    def add_arguments(self, parser):
        parser.add_argument("--jshint-exclude",
                            dest="jshint_exclude", default="",
                            help="Exclude patterns")

    def run(self, apps_locations, **options):
        output = codecs.open(os.path.join(options['output_dir'], 'jshint.xml'), 'w', 'utf-8')

        files = list(
            static_files_iterator(apps_locations + list(getattr(settings, 'STATICFILES_DIRS', [])),
                                  extension='.js',
                                  ignore_patterns=options['jshint_exclude'].split(',')))

        cmd = ['jshint', '--reporter=jslint'] + files

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        jshint_output, err = process.communicate()
        retcode = process.poll()
        if retcode not in [0, 1, 2]:  # normal jshint return codes
            raise subprocess.CalledProcessError(retcode, cmd, output='{}\n\n{}'.format(output, err))

        output.write(jshint_output.decode('utf-8'))
        output.close()
