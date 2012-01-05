# -*- coding: utf-8 -*-
from optparse import make_option
from django_jenkins.management.commands import TaskListCommand

class Command(TaskListCommand):
    help = "Run lettuce tests"

    def get_task_list(self):
        return ('django_jenkins.tasks.lettuce_tests',)
