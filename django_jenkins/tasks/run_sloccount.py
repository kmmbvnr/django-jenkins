# -*- coding: utf-8 -*-
import os
import subprocess


class Reporter(object):
    def run(self, apps_locations, **options):
        output = open(os.path.join(options['output_dir'], 'sloccount.report'), 'w')
        cmd = ['sloccount', "--duplicates", "--wide", "--details"] + apps_locations

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        report_output, err = process.communicate()

        retcode = process.poll()
        if retcode not in [0]:  # normal sloccount return codes
            raise subprocess.CalledProcessError(retcode, cmd, output='{}\n\n{}'.format(output, err))

        output.write(report_output.decode('utf-8'))
        output.close()
