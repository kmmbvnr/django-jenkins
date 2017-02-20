# -*- coding: utf-8 -*-
import os
import subprocess
from django.conf import settings


class Reporter(object):
    def run(self, apps_locations, **options):
        output = open(os.path.join(options['output_dir'], 'mypy.report'), 'w')
        cmd = [settings.MYPY_PATH, '-s', *apps_locations]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        report_output, err = process.communicate()

        retcode = process.poll()
        if retcode not in [0, 1]:  # normal mypy return codes
            raise subprocess.CalledProcessError(retcode, cmd, output='%s\n%s' % (report_output, err))

        output.write(report_output.decode('utf-8'))
        output.close()
