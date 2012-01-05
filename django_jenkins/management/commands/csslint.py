# -*- coding: utf-8; mode: django -*-
from optparse import make_option
from django_jenkins.management.commands import TaskListCommand


class Command(TaskListCommand):
    help = "Run csslint over project apps"
    args = '[appname ...]'
    option_list = TaskListCommand.option_list + (
        make_option('--csslint-file-output', action='store_true', dest='csslint_file_output', default=False,
            help='Store csslint report in file'),
    )

    def get_task_list(self):
        return ('django_jenkins.tasks.run_csslint',)
