# -*- coding: utf-8 -*-
from django_jenkins.management.commands import TaskListCommand

class Command(TaskListCommand):
    help = "Run windmill unittests"
 
    def get_task_list(self):
        return ('django_jenkins.tasks.windmill_tests',)

