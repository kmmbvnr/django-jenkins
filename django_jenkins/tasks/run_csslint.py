# -*- coding: utf-8; mode: django -*-
import os
import subprocess
import codecs
from optparse import make_option
from django.conf import settings
from django_jenkins.tasks import static_files_iterator


class Reporter(object):
    option_list = (
        make_option("--csslint-exclude",
                    dest="csslint_exclude", default=".min.css",
                    help="Comma separated exclude file patterns"),
        make_option("--csslint-ignore",
                    dest="csslint_ignore", default="",
                    help="CSSLint Ignore rules")
    )

    def run(self, apps_locations, **options):
        output = codecs.open(os.path.join(options['output_dir'], 'csslint.report'), 'w', 'utf-8')

        files = list(
            static_files_iterator(apps_locations + list(getattr(settings, 'STATICFILES_DIRS', [])),
                                  extension='.css',
                                  ignore_patterns=options['csslint_exclude'].split(',')))

        if files:
            cmd = ['csslint', '--format=lint-xml'] + files

            if options['csslint_ignore']:
                cmd += ['--ignore=%s' % options['csslint_ignore']]

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            process_output, err = process.communicate()
            retcode = process.poll()
            if retcode not in [0, 1]:  # normal csslint return codes
                raise subprocess.CalledProcessError(retcode, cmd, output=output + '\n' + err)

            output.write(process_output.decode('utf-8'))
        else:
            output.write('<?xml version="1.0" encoding='
                         '"utf-8"?><lint></lint>')

        output.close()
