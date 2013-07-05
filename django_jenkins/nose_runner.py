import os
import sys
from django.utils.unittest import TextTestRunner
from django_jenkins.runner import CITestSuiteRunner
from django_jenkins import signals
from django_jenkins.runner import XMLTestResult
from django_nose.runner import BasicNoseRunner, _get_plugins_from_settings
from django_nose.plugin import DjangoSetUpPlugin, ResultPlugin, TestReorderer
from nose.config import Config, all_config_files
from nose.plugins.manager import DefaultPluginManager
import nose


class XMLTestResult(XMLTestResult):
    def test_case_name(self, test):
        return super(XMLTestResult, self).test_case_name(test.test)


class XMLTextNoseTestRunner(nose.core.TextTestRunner):
    """Test runner that uses nose's TextTestResult to enable errorClasses,
    as well as providing hooks for plugins to override or replace the test
    output stream, results, and the test case itself.
    """

    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1,
                 config=None):
        if config is None:
            config = Config()
        self.config = config
        TextTestRunner.__init__(self, stream, descriptions, verbosity, buffer=True)

    def _makeResult(self):
        return XMLTestResult(self.stream,
                             self.descriptions,
                             self.verbosity,
                             )

    def run(self, test):
        """Overrides to provide plugin hooks and defer all output to
        the test result class.
        """
        wrapper = self.config.plugins.prepareTest(test)
        if wrapper is not None:
            test = wrapper

        # plugins can decorate or capture the output stream
        wrapped = self.config.plugins.setOutputStream(self.stream)
        if wrapped is not None:
            self.stream = wrapped

        result = self._makeResult()
        result.buffer = self.buffer
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
            else:
                result.printErrors()
        result.printErrors()
        self.config.plugins.finalize(result)
        return result


class CINoseTestSuiteRunner(CITestSuiteRunner, BasicNoseRunner):
    """
    Continuous integration test runner
    """

    def run_suite(self, nose_argv):
        signals.before_suite_run.send(sender=self)
        result_plugin = ResultPlugin()
        plugins_to_add = [DjangoSetUpPlugin(self),
                          result_plugin,
                          TestReorderer()]

        for plugin in _get_plugins_from_settings():
            plugins_to_add.append(plugin)

        cfg_files = all_config_files()
        manager = DefaultPluginManager()
        config = Config(env=os.environ, files=cfg_files, plugins=manager)
        config.plugins.addPlugins(plugins=plugins_to_add)
        text_test_runner = XMLTextNoseTestRunner(config=config, verbosity=self.verbosity)
        nose.core.TestProgram(argv=nose_argv,
                              exit=False,
                              config=config,
                              testRunner=text_test_runner)
        result = result_plugin.result

        if self.with_reports:
            result.dump_xml(self.output_dir)
        signals.after_suite_run.send(sender=self)
        return result

    def run_tests(self, test_labels, extra_tests=None):
        argv = sys.argv[:2]
        sys.argv, argv = argv, sys.argv
        result = BasicNoseRunner.run_tests(self, test_labels, extra_tests=None)
        sys.argv = argv
        return result
