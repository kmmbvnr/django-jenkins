# -*- coding: utf-8 -*-
from optparse import make_option
from django.conf import settings
from django.utils.importlib import import_module
from django_jenkins.management.commands import TaskListCommand


class Command(TaskListCommand):
    help = "Run django test suite using jenkins test runner"
    args = '[appname ...]'
    option_list = TaskListCommand.option_list + (
        make_option('--with-reports', action='store_true',
                    dest='with_reports', default=False,
                help='Create xunit reports files'),
        make_option("--coverage-html-report",
                    dest="coverage_html_report_dir",
                    default="",
                help="Enables code coverage and creates html coverage report"),
    )

    def get_tasks(self, *test_labels, **options):
        if options.get('coverage_html_report_dir',
                       getattr(settings, 'COVERAGE_HTML_REPORT', False)):
            self.tasks_cls.append(
                    import_module('django_jenkins.tasks.with_coverage').Task)
        return [task_cls(test_labels, options) for task_cls in self.tasks_cls]

    def get_task_list(self):
        enabled_tasks = getattr(settings, 'JENKINS_TASKS', ())

        tasks = []

        if 'django_jenkins.tasks.with_local_celery' in enabled_tasks:
            tasks.append('django_jenkins.tasks.with_local_celery')

        return tasks
