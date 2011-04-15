# -*- coding: utf-8 -*-
from optparse import make_option
from django_jenkins.management.commands import TaskListCommand


class Command(TaskListCommand):
    help = "Run pyflakes over project apps"
    args = '[appname ...]'
    option_list = TaskListCommand.option_list + (
        make_option('--pyflakes-file-output', action='store_true', dest='pyflakes_file_output', default=False,
            help='Store pep8 report in file'),
    )

    def get_task_list(self):
        return ('django_jenkins.tasks.run_pyflakes',)
