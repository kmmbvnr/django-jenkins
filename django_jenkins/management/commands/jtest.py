# -*- coding: utf-8 -*-
from optparse import make_option
from django_jenkins.management.commands import TaskListCommand


class Command(TaskListCommand):
    help = "Run django test suite using jenkins test runner"
    args = '[appname ...]'
    option_list = TaskListCommand.option_list + (
        make_option('--with-reports', action='store_true', dest='with_reports', default=False,
            help='Create xunit reports files'),
    )

    def get_task_list(self):
        return ('django_jenkins.tasks.django_tests',)
