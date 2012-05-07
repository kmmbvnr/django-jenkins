# -*- coding: utf-8; mode: django -*-
"""
Store and view task results data in standalone ci
"""
import math
from pygooglechart import Axis, SimpleLineChart


class BaseView(object):
    """
    Base class for standalone.ci view
    """
    def get_build_data(self, tasks, runner):
        """
        Extrats current build ci data 
        """
        return {}

    def collect_build_data(self, build_data):
        """
        Collect build data for view
        """

    def build_chart(self, start_build_id, end_build_id):
        """
        Returns pygooglechart instance with build data
        """

        
class TestView(BaseView):
    def __init__(self):
        self.successes = []
        self.failures = []
        self.errors = []

    def get_build_data(self, tasks, runner):
        test_result = self.test_runner.result

        result = {}
        result['tests-successes'] = len(test_result.successes)
        result['tests-failures'] = len(test_result.failures)
        result['tests-errors'] = len(test_result.errors)
        return result

    def collect_build_data(self, build_data):
        self.successes.append(build_data['tests-successes'])
        self.failures.append(build_data['tests-failures'])
        self.errors.append(build_data['tests-errors'])
        
    def build_chart(self, start_build_id, end_build_id):
        tests_chart = SimpleLineChart(400, 250)
        all_fails = [f+e for f,e in zip(self.failures, self.errors)]
        all_results = [s+af for s,af in zip(self.successes, all_fails)]

        # axis
        max_tests = max(all_results)
        step = round(max_tests/10, 1-len(str(max_tests/10)))
        total_steps = math.ceil(1.0 * max_tests/step)
        tests_chart.set_axis_labels(Axis.LEFT, xrange(0, step*(total_steps+1), step))
        tests_chart.set_axis_labels(Axis.BOTTOM, xrange(start_build_id, end_build_id+1))
        tests_chart.set_grid(0, step/2, 5, 5)

        # First value - allowed maximum
        tests_chart.add_data([step*total_steps] * 2)
        # All tests, failures and errors, errors
        tests_chart.add_data(all_results)
        tests_chart.add_data(all_fails)
        tests_chart.add_data(self.errors)
        # Last value is the lowest in the Y axis.
        tests_chart.add_data([0] * 2)

        # Fill colors
        tests_chart.set_colours(['FFFFFF', '00FF00', 'FF0000', '0000FF'])
        tests_chart.add_fill_range('00FF00', 1, 2)
        tests_chart.add_fill_range('FF0000', 2, 3)
        tests_chart.add_fill_range('0000FF', 3, 4)

        return tests_chart


class ViolationsView(BaseView):
    pass
