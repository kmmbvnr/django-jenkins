# -*- coding: utf-8 -*-
import io
import sys
from xml.etree import ElementTree as ET

from django.core import mail
from django.test import TestCase
from unittest import skip

from django.test import LiveServerTestCase
from pyvirtualdisplay import Display
from selenium import webdriver

from django_jenkins.runner import EXMLTestResult


class SaintyChecks(TestCase):
    # @classmethod
    # def setUpClass(cls):
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

    # def test_failure(self):
    #    raise Exception("Ups, should be disabled")


class EXMLTestResultTests(TestCase):
    def setUp(self):
        self.exml_result = EXMLTestResult(None, None, 1)
        self.exml_result.startTestRun()
        self.result_element = ET.SubElement(self.exml_result.tree, 'result')

    def test_non_ascii_traceback(self):
        try:
            self.explode_with_unicode_traceback()
        except ValueError:
            err = sys.exc_info()
        else:
            self.fail()

        self.exml_result._add_tb_to_test(TestCase('fail'), self.result_element, err)

        output = self.write_element(self.result_element)

        self.assert_(output)

    def test_non_ascii_message(self):
        try:
            self.explode_with_unicode_message()
        except ValueError:
            err = sys.exc_info()
        else:
            self.fail()

        self.exml_result._add_tb_to_test(TestCase('fail'), self.result_element, err)

        output = self.write_element(self.result_element)

        self.assert_(output)

    def write_element(self, element):
        # write out the element the way that our TestResult.dump_xml does.
        # (except not actually to disk.)
        tree = ET.ElementTree(element)
        output = io.BytesIO()
        # this bit blows up if components of the output are byte-strings with non-ascii content.
        tree.write(output, encoding='utf-8')
        output_bytes = output.getvalue()
        return output_bytes

    def explode_with_unicode_traceback(self):
        # The following will result in an ascii error message, but the traceback will contain the
        # full source line, including the comment's non-ascii characters.
        raise ValueError("dead")  # "⚠ Not enough ☕"

    def explode_with_unicode_message(self):
        # This source code has only ascii, the exception has a non-ascii message.
        raise ValueError(u"\N{BIOHAZARD SIGN} Too much \N{HOT BEVERAGE}")


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.display = Display(visible=0, size=(1024, 768))
        cls.display.start()
        cls.selenium = webdriver.Firefox()
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(SeleniumTests, cls).tearDownClass()
        cls.selenium.quit()
        cls.display.stop()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/test_click/'))
        self.selenium.find_element_by_id("wm_click").click()
        self.assertEqual('Button clicked', self.selenium.find_element_by_id("wm_target").text)
