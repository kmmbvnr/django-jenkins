# -*- coding: utf-8 -*-
from optparse import make_option
from django_jenkins.management.commands import TaskListCommand


class Command(TaskListCommand):
    help = "Run testem over project apps"
    args = '[appname ...]'
    option_list = TaskListCommand.option_list + (
        make_option('--testem-file-output', action='store_true', dest='testem_file_output', default=False,
            help='Store testem report in files'),
    )

    def get_task_list(self):
        return ('django_jenkins.tasks.run_testem',)
