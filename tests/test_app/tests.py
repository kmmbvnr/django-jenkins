# -*- coding: utf-8 -*-
import sys
from django.core import mail
from django.test import TestCase
from django.utils.unittest import skip
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class SaintyChecks(TestCase):
    #@classmethod
    #def setUpClass(cls):
    #    raise Exception("Ups, should be disabled")

    def test_mailbox_stubs_not_broken(self):
        print("Testing mailbox django stubs")
        mail.send_mail('Test subject', 'Test message', 'nobody@kenkins.com',
                       ['somewhere@nowhere.com'])
        self.assertTrue(1, len(mail.outbox))

    @skip("Check skiped test")
    def test_is_skipped(self):
        print("This test should be skipped")

    def test_junit_xml_with_utf8_stdout_and_stderr(self):
        sys.stdout.write('\xc4\x85')
        sys.stderr.write('\xc4\x85')

    def test_junit_xml_with_invalid_stdout_and_stderr_encoding(self):
        sys.stdout.write('\xc4')
        sys.stderr.write('\xc4')


    #def test_failure(self):
    #    raise Exception("Ups, should be disabled")


class SeleniumTests(LiveServerTestCase):
    fixtures = ['default_users.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(SeleniumTests, cls).tearDownClass()
        cls.selenium.quit()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/test_click/'))
        self.selenium.find_element_by_id("wm_click").click()
        self.assertEqual('Button clicked', self.selenium.find_element_by_id("wm_target").text)
