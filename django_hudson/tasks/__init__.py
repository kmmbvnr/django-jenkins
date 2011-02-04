# -*- coding: utf-8 -*-
class BaseTask(object):
    """
    Base interface for ci tasks
    """
    def add_options(self, group):
        pass

    def configure(self, test_modules, options):
        pass

    def run_task(self):
        pass

    def after_tasks_run(self):
        pass

