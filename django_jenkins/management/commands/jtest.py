# -*- coding: utf-8 -*-
from django_jenkins.management.commands import TaskListCommand


class Command(TaskListCommand):
    help = "Run django test suite using jenkins test runner"
    args = '[appname ...]'

    def get_task_list(self):
        return ('django_jenkins.tasks.django_tests',)
