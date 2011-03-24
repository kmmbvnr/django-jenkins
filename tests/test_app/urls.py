# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
     url(r'^wm_test_click/$', 'django.views.generic.simple.direct_to_template',
         {'template': 'test_app/wm_test_click.html'}, name='wm_test_click')
)
