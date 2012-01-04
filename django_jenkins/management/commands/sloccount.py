# -*- coding: utf-8; mode: django -*-
from optparse import make_option
from django_jenkins.management.commands import TaskListCommand


class Command(TaskListCommand):
    help = "Run sloccount over project apps"
    args = '[appname ...]'
    option_list = TaskListCommand.option_list + (
        make_option('--sloccount-file-output', action='store_true', dest='sloccount_file_output', default=False,
            help='Store sloccount report in file'),
    )

    def get_task_list(self):
        return ('django_jenkins.tasks.run_sloccount',)
