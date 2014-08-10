from django.db import models


class TestDirModel(models.Model):
    test_text = models.CharField(max_length=250)

    class Meta:
        app_label = 'test_app_dirs'