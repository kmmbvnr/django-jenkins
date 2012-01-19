# -*- coding: utf-8; mode: django -*-
import os
import sys
from django_jenkins.standalone.storage import Storage
from django_jenkins.management.commands.jenkins import Command as BaseCICommand


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

        # TODO Here jenkins-task views come to play

        # tests
        test_result = self.test_runner.result        
        build_data['tests-successes'] = len(test_result.successes)
        build_data['tests-failures'] = len(test_result.failures)
        build_data['tests-errors'] = len(test_result.errors)

        # End jenkins-task views

        storage['build-%d' % build_id] = build_data
        storage['last_build_id']  = build_id
        storage.close()

        if result:
            sys.exit(1)

