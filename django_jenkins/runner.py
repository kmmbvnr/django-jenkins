# -*- coding: utf-8; mode: django -*-
import os
import sys
import time

from xml.etree import ElementTree as ET
from django.conf import settings
from django.utils.encoding import smart_text
from django.test.testcases import TestCase
from django.utils.unittest import TextTestResult, TextTestRunner

try:
    # Django 1.6
    from django.test.runner import DiscoverRunner
except ImportError:
    # Fallback to third-party app on Django 1.5
    try:
        from discover_runner.runner import DiscoverRunner
    except ImportError:
        import warnings
        warnings.warn(
            "Directory-only tests are ignored. Install django-discover-runner to enable it",
            UserWarning)
        from django.test.simple import DjangoTestSuiteRunner as DiscoverRunner

try:
    from django.test.simple import reorder_suite
except ImportError:
    from django.test.runner import reorder_suite

from django_jenkins import signals


class EXMLTestResult(TextTestResult):
    def __init__(self, *args, **kwargs):
        self.case_start_time = None
        self.run_start_time = None
        self.tree = None
        super(EXMLTestResult, self).__init__(*args, **kwargs)

    def startTest(self, test):
        self.case_start_time = time.time()
        super(EXMLTestResult, self).startTest(test)

    def startTestRun(self):
        self.tree = ET.Element('testsuite')
        self.run_start_time = time.time()
        super(EXMLTestResult, self).startTestRun()

    def addSuccess(self, test):
        self.testcase = self._make_testcase_element(test)
        super(EXMLTestResult, self).addSuccess(test)

    def addFailure(self, test, err):
        self.testcase = self._make_testcase_element(test)
        test_result = ET.SubElement(self.testcase, 'failure')
        self._add_tb_to_test(test, test_result, err)
        super(EXMLTestResult, self).addFailure(test, err)

    def addError(self, test, err):
        self.testcase = self._make_testcase_element(test)
        test_result = ET.SubElement(self.testcase, 'error')
        self._add_tb_to_test(test, test_result, err)
        super(EXMLTestResult, self).addError(test, err)

    def addUnexpectedSuccess(self, test):
        self.testcase = self._make_testcase_element(test)
        test_result = ET.SubElement(self.testcase, 'skipped')
        test_result.set('message', 'Test Skipped: Unexpected Success')
        super(EXMLTestResult, self).addUnexpectedSuccess(test)

    def addSkip(self, test, reason):
        self.testcase = self._make_testcase_element(test)
        test_result = ET.SubElement(self.testcase, 'skipped')
        test_result.set('message', 'Test Skipped: %s' % reason)
        super(EXMLTestResult, self).addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        self.testcase = self._make_testcase_element(test)
        test_result = ET.SubElement(self.testcase, 'skipped')
        self._add_tb_to_test(test, test_result, err)
        super(EXMLTestResult, self).addExpectedFailure(test, err)

    def stopTest(self, test):
        if self.buffer:
            output = sys.stdout.getvalue() if hasattr(sys.stdout, 'getvalue') else ''
            if output:
                sysout = ET.SubElement(self.testcase, 'system-out')
                sysout.text = smart_text(output, errors='ignore')

            error = sys.stderr.getvalue() if hasattr(sys.stderr, 'getvalue') else ''
            if error:
                syserr = ET.SubElement(self.testcase, 'system-err')
                syserr.text = smart_text(error, errors='ignore')

        super(EXMLTestResult, self).stopTest(test)

    def stopTestRun(self):
        run_time_taken = time.time() - self.run_start_time
        self.tree.set('name', 'Django Project Tests')
        self.tree.set('errors', str(len(self.errors)))
        self.tree.set('failures', str(len(self.failures)))
        self.tree.set('skips', str(len(self.skipped)))
        self.tree.set('tests', str(self.testsRun))
        self.tree.set('time', "%.3f" % run_time_taken)
        super(EXMLTestResult, self).stopTestRun()

    def _make_testcase_element(self, test):
        time_taken = time.time() - self.case_start_time
        classname = ('%s.%s' % (test.__module__, test.__class__.__name__)).split('.')
        testcase = ET.SubElement(self.tree, 'testcase')
        testcase.set('time', "%.6f" % time_taken)
        testcase.set('classname', '.'.join(classname))
        testcase.set('name', test._testMethodName)
        return testcase

    def _add_tb_to_test(self, test, test_result, err):
        '''Add a traceback to the test result element'''
        exc_class, exc_value, tb = err
        tb_str = self._exc_info_to_string(err, test)
        test_result.set('type', '%s.%s' % (exc_class.__module__, exc_class.__name__))
        test_result.set('message', str(exc_value))
        test_result.text = tb_str

    def dump_xml(self, output_dir):
        """
        Dumps test result to xml
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output = ET.ElementTree(self.tree)
        output.write(os.path.join(output_dir, 'junit.xml'), encoding="utf-8")


class CITestSuiteRunner(DiscoverRunner):
    """
    Continuous integration test runner
    """
    def __init__(self, output_dir, with_reports=True, debug=False, test_all=False, **kwargs):
        super(CITestSuiteRunner, self).__init__(**kwargs)
        self.with_reports = with_reports
        self.output_dir = output_dir
        self.debug = debug
        self.test_all = test_all

    def setup_test_environment(self, **kwargs):
        super(CITestSuiteRunner, self).setup_test_environment()
        signals.setup_test_environment.send(sender=self)

    def teardown_test_environment(self, **kwargs):
        super(CITestSuiteRunner, self).teardown_test_environment()
        signals.teardown_test_environment.send(sender=self)

    def setup_databases(self):
        if 'south' in settings.INSTALLED_APPS:
            from south.management.commands import (
                patch_for_test_db_setup  # pylint: disable=F0401
            )
            patch_for_test_db_setup()
        return super(CITestSuiteRunner, self).setup_databases()

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        if not test_labels and not self.test_all:
            if hasattr(settings, 'PROJECT_APPS'):
                test_labels = settings.PROJECT_APPS

        suite = super(CITestSuiteRunner, self).build_suite(test_labels, extra_tests=None, **kwargs)
        signals.build_suite.send(sender=self, suite=suite)
        return reorder_suite(suite, getattr(self, 'reorder_by', (TestCase,)))

    def run_suite(self, suite, **kwargs):
        signals.before_suite_run.send(sender=self)
        result = TextTestRunner(buffer=not self.debug,
                                resultclass=EXMLTestResult,
                                verbosity=self.verbosity).run(suite)
        if self.with_reports:
            result.dump_xml(self.output_dir)
        signals.after_suite_run.send(sender=self)
        return result

