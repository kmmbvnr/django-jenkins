# -*- coding: utf-8 -*-
from django.test import TestCase
from windmill.authoring import WindmillTestClient
from django_hudson.tasks import windmill_tests

class TestWMClickPage(TestCase):
    def _test_open_yaru(self):
        client = WindmillTestClient(__name__)
        client.open(url=u'http://ya.ru')
        client.waits.forPageLoad(timeout=u'8000')
        client.click(id='sethome')

    def test_wmclick(self):
        client = WindmillTestClient(__name__)
        client.open(url=u'http://127.0.0.2:%d/wm_test_click' % windmill_tests.TEST_SERVER_PORT)
        client.waits.forPageLoad(timeout=u'5000')
        client.click(id='wm_click')
        client.asserts.assertText(validator=u'Button clicked', id=u'wm_target')

