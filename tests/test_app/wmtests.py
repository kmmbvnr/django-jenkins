# -*- coding: utf-8 -*-
from django_jenkins.tasks.windmill_tests import WindmillTestCase

class TestWMClickPage(WindmillTestCase):
    def test_wmclick(self):
        self.windmill.open('wm_test_click')
        self.windmill.waits.forPageLoad(timeout=u'5000')
        self.windmill.click(id='wm_click')
        self.windmill.asserts.assertText(validator=u'Button clicked', id=u'wm_target')

