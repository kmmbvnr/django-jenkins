# -*- coding: utf-8 -*-
from django.conf import settings
from django_hudson.management.commands import TaskListCommand

class Command(TaskListCommand):
    help = "Run CI process"
    args = '[appname ...]'
 
    def get_task_list(self):
        return getattr(settings, 'HUDSON_TASKS',
                       ('django_hudson.tasks.run_pylint',
                        'django_hudson.tasks.with_coverage',
                        'django_hudson.tasks.run_xmltest',))

