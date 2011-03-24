# -*- coding: utf-8 -*-
from django.conf import settings
from django_jenkins.management.commands import TaskListCommand


class Command(TaskListCommand):
    help = "Run CI process"
    args = '[appname ...]'

    def get_task_list(self):
        return getattr(settings, 'JENKINS_TASKS',
                       ('django_jenkins.tasks.run_pylint',
                        'django_jenkins.tasks.with_coverage',
                        'django_jenkins.tasks.django_tests',))
