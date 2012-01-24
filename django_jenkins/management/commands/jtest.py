# -*- coding: utf-8 -*-
from optparse import make_option
from django.conf import settings
from django_jenkins.management.commands import TaskListCommand


class Command(TaskListCommand):
    help = "Run django test suite using jenkins test runner"
    args = '[appname ...]'
    option_list = TaskListCommand.option_list + (
        make_option('--with-reports', action='store_true', dest='with_reports', default=False,
            help='Create xunit reports files'),
    )

    def get_task_list(self):
        enabled_tasks = getattr(settings, 'JENKINS_TASKS', ())

        tasks = ['django_jenkins.tasks.django_tests']
        if 'django_jenkins.tasks.lettuce_tests' in enabled_tasks:
            tasks.append('django_jenkins.tasks.lettuce_tests')
        if 'django_jenkins.tasks.with_local_celery' in enabled_tasks:
            tasks.append('django_jenkins.tasks.with_local_celery')
        return tasks

