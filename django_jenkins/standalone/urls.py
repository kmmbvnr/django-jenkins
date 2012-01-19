# -*- coding: utf-8; mode: django -*-
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('django_jenkins.standalone.views',
    url(r'^$', 'index', name="ci_index"),
)

