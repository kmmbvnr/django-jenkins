# -*- coding: utf-8 -*-
from django.test import TestCase
from windmill.authoring import WindmillTestClient


class TestWMClickPage(TestCase):
    def test_open_yaru(self):
        client = WindmillTestClient(__name__)
        client.open(url=u'http://ya.ru')
        client.waits.forPageLoad(timeout=u'8000')
        client.click(id='sethome')

    def _test_wmclick(self):
        client = WindmillTestClient(__name__)
        client.open(url=u'http://127.0.0.1:8081/wm_test_click')
        #client.click(id='wm_click')
        client.waits.forPageLoad(timeout=u'5000')

