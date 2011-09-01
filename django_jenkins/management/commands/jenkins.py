# -*- coding: utf-8 -*-
from django.conf import settings
from django_jenkins.management.commands import TaskListCommand
from multiprocessing import Pool

def run_parallel_task(task_cls, test_labels, options):
    task_cls(test_labels, options).run()

class Command(TaskListCommand):
    help = "Run CI process"
    args = '[appname ...]'

    def get_task_list(self):
        return getattr(settings, 'JENKINS_TASKS',
                       ('django_jenkins.tasks.run_pylint',
                        'django_jenkins.tasks.with_coverage',
                        'django_jenkins.tasks.django_tests',))

    def handle_static_tasks(self, test_labels, options):
        self.pool = Pool()
        for task in self.tasks:
            if hasattr(task, 'run'):
                self.pool.apply_async(run_parallel_task, args=(task.__class__, test_labels, options))
        self.pool.close()

    def finish_static_tasks(self):
        self.pool.join()