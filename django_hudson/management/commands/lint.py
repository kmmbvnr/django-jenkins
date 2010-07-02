# -*- coding: utf-8 -*-
import os, sys
from optparse import make_option
from pylint import lint
from pylint.reporters.text import ParseableTextReporter
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "proccess django application with pylint"

    option_list = BaseCommand.option_list + (
        make_option('--output', dest='output_file', default='',
                    help='Redirect pylint report to file'),
    )

    def handle(self, *args, **options):
        output_file=options.get('output_file')
        if output_file:
            output = open(output_file, 'w')
        else:
            output = sys.stdout

        config = "--rcfile=" + Command.default_config_path()
        lint.Run([config] + list(args), reporter=ParseableTextReporter(output=output), exit=False)

    @staticmethod
    def default_config_path():
        root_dir = os.path.normpath(os.path.dirname(__file__))
        return os.path.join(root_dir, 'pylint.rc')
