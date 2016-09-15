# -*- coding: utf-8; mode: django -*-
import os
import subprocess
import codecs

from django.conf import settings
from django_jenkins.tasks import static_files_iterator


class Reporter(object):
    def add_arguments(self, parser):
        parser.add_argument("--scss-lint-exclude",
                            dest="scss_lint_exclude", default="",
                            help="Comma separated exclude file patterns")

    def run(self, apps_locations, **options):
        output = codecs.open(os.path.join(options['output_dir'], 'scss-lint.xml'), 'w', 'utf-8')

        files = list(
            static_files_iterator(apps_locations + list(getattr(settings, 'STATICFILES_DIRS', [])),
                                  extension='.scss',
                                  ignore_patterns=options['scss_lint_exclude'].split(',')))

        if files:
            cmd = ['scss-lint', '--require=scss_lint_reporter_checkstyle', '--format=Checkstyle'] + files

            config_file = getattr(settings, 'SCSS_LINT_CONFIG_FILE', None)
            if config_file:
                cmd += ['--config=%s' % config_file]

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            process_output, err = process.communicate()
            retcode = process.poll()
            if retcode not in [0, 1, 2]:  # normal scss-lint return codes
                raise subprocess.CalledProcessError(retcode, cmd, output='{}\n\n{}'.format(output, err))

            output.write(process_output.decode('utf-8'))
        else:
            output.write('<?xml version="1.0" encoding='
                         '"utf-8"?><lint></lint>')

        output.close()
