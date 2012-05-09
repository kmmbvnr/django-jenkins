# -*- coding: utf-8; mode: django -*-
"""
View for tasks with tests runner
"""
import math
import sys
from pygooglechart import Axis, SimpleLineChart
from django.template.loader import render_to_string
from django_jenkins.standalone import taskviews


class TaskDataExtract(taskviews.BaseTaskDataExtract):
    """
    Extract data from test runner tasks.
    
    Each task should have test_runner and output_file attributes
    """
    def extract_build_data(self, tasks):
        """
        Extrats current build ci data 
        """
        result = {}
        result['tests-successes'] = 0
        result['tests-failures'] = 0
        result['tests-errors'] = 0

        for task in tasks:
            test_result = task.test_runner.result
            result['tests-successes'] += len(test_result.successes)
            result['tests-failures'] += len(test_result.failures)
            result['tests-errors'] += len(test_result.errors)

        return result

    def extract_details_data(self, tasks):
        """
        Extract details view data
        """
        output = []
        for task in tasks:
            output.append(task.output_file)
        return { 'output' : output }
    

class TaskDataView(taskviews.BaseTaskDataView):
    """
    Renters html part of ci index page
    """
    def __init__(self):
        self.min_build_id, self.max_build_id = sys.max_int, 0
        self.successes = []
        self.failures = []
        self.errors = []

    def add_build_data(self, build_id, build_data):
        self.min_build_id = min(build_id, self.min_build_id)
        self.max_build_id = max(build_id, self.max_build_id)
        self.successes.append(build_data['tests-successes'])
        self.failures.append(build_data['tests-failures'])
        self.errors.append(build_data['tests-errors'])

    def build_chart(self):
        tests_chart = SimpleLineChart(400, 250)
        all_fails = [f+e for f,e in zip(self.failures, self.errors)]
        all_results = [s+af for s,af in zip(self.successes, all_fails)]

        # axis
        max_tests = max(all_results)
        step = round(max_tests/10, 1-len(str(max_tests/10)))
        total_steps = math.ceil(1.0 * max_tests/step)
        tests_chart.set_axis_labels(Axis.LEFT, xrange(0, step*(total_steps+1), step))
        tests_chart.set_axis_labels(Axis.BOTTOM, xrange(self.min_build_id, self.max_build_id+1))
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

    def render_part(self, request):
        return render_to_string('django_jenkins/tests_part.html',
            { 'chart' : self.build_chart(),
              'title' : 'Tests result' })


class TaskDetailView(taskviews.BaseTaskDetailView):
    """
    Renders build task detail page
    """
    def view(request, build_id, build_data):
        pass

