from django.db import models
from test_app.not_for_coverage import one, two  # NOQA


class TestModel(models.Model):
    test_text = models.CharField(max_length=250)
