# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^test_click/$', TemplateView.as_view(template_name='test_app/wm_test_click.html'),
        name='wm_test_click')
]
