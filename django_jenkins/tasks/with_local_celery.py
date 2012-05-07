# -*- coding: utf-8; mode: django -*-
from django.conf import settings
from django_jenkins.tasks import BaseTask


class Task(BaseTask):
    """
    Run all celery tasks locally, not in a worker.
    """

    def setup_test_environment(self, **kwargs):
        settings.CELERY_ALWAYS_EAGER = True
        settings.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

