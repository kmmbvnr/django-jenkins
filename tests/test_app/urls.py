# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
     url(r'^ci/$', include('django_jenkins.standalone.urls')),
)

