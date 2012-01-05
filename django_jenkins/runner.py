# -*- coding: utf-8 -*-
"""
Extensible dango test runner
"""
import os
import sys
import time
import unittest
from cStringIO import StringIO
from unittest import _TextTestResult, TestResult
from xml.dom.minidom import Document
from django.conf import settings
from django.test import TestCase
from django.test.simple import DjangoTestSuiteRunner, reorder_suite
from django_jenkins import signals
try:
    from django.test.simple import TextTestRunner as TestRunner
except ImportError:
    from django.test.simple import DjangoTestRunner as TestRunner


class _TestInfo(object):
    """This class is used to keep useful information about the execution of a
    test method.
    """

    # Possible test outcomes
    (SUCCESS, FAILURE, ERROR) = range(3)

    def __init__(self, test_result, test_method, outcome=SUCCESS, err=None):
        "Create a new instance of _TestInfo."
        self.test_result = test_result
        self.test_method = test_method
        self.outcome = outcome
        self.err = err

    def get_elapsed_time(self):
        """Return the time that shows how long the test method took to
        execute.
        """
        return self.test_result.stop_time - self.test_result.start_time

    def get_description(self):
        "Return a text representation of the test method."
        return self.test_result.getDescription(self.test_method)

    def get_error_info(self):
        """Return a text representation of an exception thrown by a test
        method.
        """
        if not self.err:
            return ''

        return self.test_result._exc_info_to_string(self.err, \
            self.test_method)


class _XMLTestResult(_TextTestResult):
    """
    A test result class that can express test results in a XML report.

    Used by XMLTestRunner.
    """
    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1, \
                 elapsed_times=True):
        "Create a new instance of _XMLTestResult."
        _TextTestResult.__init__(self, stream, descriptions, verbosity)
        self.successes = []
        self.callback = None
        self.elapsed_times = elapsed_times

    def _prepare_callback(self, test_info, target_list, verbose_str, \
                          short_str):
        """Append a _TestInfo to the given target list and sets a callback
        method to be called by stopTest method.
        """
        target_list.append(test_info)

        def callback():
            """This callback prints the test method outcome to the stream,
            as well as the elapsed time.
            """

            # Ignore the elapsed times for a more reliable unit testing
            if not self.elapsed_times:
                self.start_time = self.stop_time = 0

            if self.showAll:
                self.stream.writeln('%s (%.3fs)' % \
                    (verbose_str, test_info.get_elapsed_time()))
            elif self.dots:
                self.stream.write(short_str)
        self.callback = callback

    def startTest(self, test):
        "Called before execute each test method."
        self.start_time = time.time()
        TestResult.startTest(self, test)

        if self.showAll:
            self.stream.write('  ' + self.getDescription(test))
            self.stream.write(" ... ")

    def stopTest(self, test):
        "Called after execute each test method."
        _TextTestResult.stopTest(self, test)
        self.stop_time = time.time()

        if self.callback and callable(self.callback):
            self.callback()
            self.callback = None

    def addSuccess(self, test):
        "Called when a test executes successfully."
        self._prepare_callback(_TestInfo(self, test), \
            self.successes, 'OK', '.')

    def addFailure(self, test, err):
        "Called when a test method fails."
        self._prepare_callback(_TestInfo(self, test, _TestInfo.FAILURE, err), \
            self.failures, 'FAIL', 'F')

    def addError(self, test, err):
        "Called when a test method raises an error."
        self._prepare_callback(_TestInfo(self, test, _TestInfo.ERROR, err), \
            self.errors, 'ERROR', 'E')

    def printErrorList(self, flavour, errors):
        "Write some information about the FAIL or ERROR to the stream."
        for test_info in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln('%s [%.3fs]: %s' % \
                (flavour, test_info.get_elapsed_time(), \
                test_info.get_description()))
            self.stream.writeln(self.separator2)
            self.stream.writeln('%s' % test_info.get_error_info())

    def _get_info_by_testcase(self):
        """This method organizes test results by TestCase module. This
        information is used during the report generation, where a XML report
        will be generated for each TestCase.
        """
        tests_by_testcase = {}

        for tests in (self.successes, self.failures, self.errors):
            for test_info in tests:
                testcase = type(test_info.test_method)

                # Ignore module name if it is '__main__'
                module = testcase.__module__ + '.'
                if module == '__main__.':
                    module = ''
                testcase_name = module + testcase.__name__

                if testcase_name not in tests_by_testcase:
                    tests_by_testcase[testcase_name] = []
                tests_by_testcase[testcase_name].append(test_info)

        return tests_by_testcase

    def _report_testsuite(suite_name, tests, xml_document):
        "Appends the testsuite section to the XML document."
        testsuite = xml_document.createElement('testsuite')
        xml_document.appendChild(testsuite)

        testsuite.setAttribute('name', suite_name)
        testsuite.setAttribute('tests', str(len(tests)))

        testsuite.setAttribute('time', '%.3f' % \
            sum(map(lambda e: e.get_elapsed_time(), tests)))

        failures = filter(lambda e: e.outcome == _TestInfo.FAILURE, tests)
        testsuite.setAttribute('failures', str(len(failures)))

        errors = filter(lambda e: e.outcome == _TestInfo.ERROR, tests)
        testsuite.setAttribute('errors', str(len(errors)))

        return testsuite

    _report_testsuite = staticmethod(_report_testsuite)

    def _test_method_name(test_method):
        "Returns the test method name."
        test_id = test_method.id()
        return test_id.split('.')[-1]

    _test_method_name = staticmethod(_test_method_name)

    def _report_testcase(suite_name, test_result, xml_testsuite, xml_document):
        "Appends a testcase section to the XML document."
        testcase = xml_document.createElement('testcase')
        xml_testsuite.appendChild(testcase)

        testcase.setAttribute('classname', suite_name)
        testcase.setAttribute('name', _XMLTestResult._test_method_name(test_result.test_method))
        testcase.setAttribute('time', '%.3f' % test_result.get_elapsed_time())

        if (test_result.outcome != _TestInfo.SUCCESS):
            elem_name = ('failure', 'error')[test_result.outcome - 1]
            failure = xml_document.createElement(elem_name)
            testcase.appendChild(failure)

            failure.setAttribute('type', test_result.err[0].__name__)
            failure.setAttribute('message', str(test_result.err[1]))

            error_info = test_result.get_error_info()
            _XMLTestResult._add_cdata(xml_document, error_info, failure)

    _report_testcase = staticmethod(_report_testcase)

    def _report_output(test_runner, xml_testsuite, xml_document):
        "Appends the system-out and system-err sections to the XML document."
        systemout = xml_document.createElement('system-out')
        xml_testsuite.appendChild(systemout)

        stdout = test_runner.stdout.getvalue()
        _XMLTestResult._add_cdata(xml_document, stdout, systemout)

        systemerr = xml_document.createElement('system-err')
        xml_testsuite.appendChild(systemerr)

        stderr = test_runner.stderr.getvalue()
        _XMLTestResult._add_cdata(xml_document, stderr, systemerr)

    _report_output = staticmethod(_report_output)

    def _add_cdata(xml_document, content, append_to=None):
        """
        Protect from CDATA inside CDATA
        """
        results = list()
        content = content.split(']]>')
        for index, entry in enumerate(content):
            if not entry:
                continue
            if index < len(content) - 1:
                entry += ']]'
            results.append(xml_document.createCDATASection(entry))
            if index < len(content) - 1:
                results.append(xml_document.createCDATASection('>'))
        if append_to:
            for result in results:
                append_to.appendChild(result)

    _add_cdata = staticmethod(_add_cdata)

    def generate_reports(self, test_runner):
        "Generates the XML reports to a given XMLTestRunner object."
        all_results = self._get_info_by_testcase()

        if not os.path.exists(test_runner.output_dir):
            os.makedirs(test_runner.output_dir)

        for suite, tests in all_results.items():
            doc = Document()

            # Build the XML file
            testsuite = _XMLTestResult._report_testsuite(suite, tests, doc)
            for test in tests:
                _XMLTestResult._report_testcase(suite, test, testsuite, doc)
            _XMLTestResult._report_output(test_runner, testsuite, doc)
            xml_content = doc.toprettyxml(indent='\t')

            report_file = file('%s%sTEST-%s.xml' % (test_runner.output_dir, os.sep, suite), 'w')
            try:
                report_file.write(xml_content)
            finally:
                report_file.close()


class XMLTestRunner(TestRunner):
    """
    A test result class that can express test results in a XML report.
    """
    def __init__(self, output_dir, debug=False, with_reports=True, **kwargs):
        super(XMLTestRunner, self).__init__(**kwargs)
        self.with_reports = with_reports
        self.debug = debug
        self.output_dir = output_dir

    def _makeResult(self):
        return _XMLTestResult(self.stream, self.descriptions, self.verbosity)

    def _patch_standard_output(self):
        """Replace the stdout and stderr streams with string-based streams
        in order to capture the tests' output.
        """
        (self.old_stdout, self.old_stderr) = (sys.stdout, sys.stderr)
        (self.stdout, self.stderr) = (StringIO(), StringIO())

        if not self.debug:
            (sys.stdout, sys.stderr) = (self.stdout, self.stderr)

    def _restore_standard_output(self):
        "Restore the stdout and stderr streams."
        (sys.stdout, sys.stderr) = (self.old_stdout, self.old_stderr)

    def run(self, test):
        try:
            self._patch_standard_output()
            result = super(XMLTestRunner, self).run(test)
            if self.with_reports:
                result.generate_reports(self)
        finally:
            self._restore_standard_output()
        return result


class CITestSuiteRunner(DjangoTestSuiteRunner):
    """
    Continues integration test runner
    """
    def __init__(self, output_dir, debug=False, with_reports=True, **kwargs):
        super(CITestSuiteRunner, self).__init__(**kwargs)
        self.with_reports = with_reports
        self.debug = debug
        self.output_dir = output_dir

    def setup_test_environment(self, **kwargs):
        super(CITestSuiteRunner, self).setup_test_environment()
        signals.setup_test_environment.send(sender=self)

    def teardown_test_environment(self, **kwargs):
        super(CITestSuiteRunner, self).teardown_test_environment()
        signals.teardown_test_environment.send(sender=self)

    def setup_databases(self):
        if 'south' in settings.INSTALLED_APPS:
            from south.management.commands import patch_for_test_db_setup  # pylint: disable=F0401
            patch_for_test_db_setup()
        return super(CITestSuiteRunner, self).setup_databases()

    def build_suite(self, test_labels, **kwargs):
        suite = unittest.TestSuite()
        signals.build_suite.send(sender=self, suite=suite)
        return reorder_suite(suite, (TestCase,))

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests=extra_tests)
        if suite.countTestCases():
            old_config = self.setup_databases()
            result = self.run_suite(suite)
            self.teardown_databases(old_config)
            self.teardown_test_environment()
            return self.suite_result(suite, result)
        else:
            self.teardown_test_environment()
            return 0

    def run_suite(self, suite, **kwargs):
        signals.before_suite_run.send(sender=self)
        result = XMLTestRunner(
            verbosity=self.verbosity,
            output_dir=self.output_dir,
            debug=self.debug,
            with_reports=self.with_reports).run(suite)
        signals.after_suite_run.send(sender=self)

        return result
