# -*- coding: utf-8; mode: django -*-
import os
import sys
from itertools import groupby
from django.utils.importlib import import_module
from django_jenkins.standalone.storage import Storage
from django_jenkins.management.commands.jenkins import Command as BaseCICommand

def task_view(task):
    return getattr(task, 'view', None)


class Command(BaseCICommand):
    help = "Run CI process, and collect data for django_jenkins.standalon"
    args = '[appname ...]'

    def handle(self, *test_labels, **options):
        storage = Storage.open()
        build_id = storage['last_build_id'] + 1

        # substitute output_dir
        options['output_dir'] = os.path.join(Storage.ci_root(), 'build-%d' % build_id)

        # run
        self.initialize(*test_labels, **options)
        result = self.test_runner.run_tests(test_labels)

        # store results and exit
        build_data = {}

        # here is jenkins-task views come to play
        build_data['views'] = []
        self.tasks.sort(key=task_view)
        for view_name, tasks in groupby(self.tasks, task_view):
            view = import_module(view_name)
            build_data[view_name] = view.get_build_data(tasks)
            build_data['views'].append(view_name)

        # tests
        #test_result = self.test_runner.result
        #build_data['tests-successes'] = len(test_result.successes)
        #build_data['tests-failures'] = len(test_result.failures)
        #build_data['tests-errors'] = len(test_result.errors)

        # End jenkins-task views

        storage['build-%d' % build_id] = build_data
        storage['last_build_id']  = build_id
        storage.close()

        if result:
            sys.exit(1)
