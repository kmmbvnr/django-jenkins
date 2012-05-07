# -*- coding: utf-8; mode: django -*-
import math
from pygooglechart import Axis, SimpleLineChart
from django.shortcuts import render
from django_jenkins.standalone.storage import Storage


def index(request):
    try:
        storage = Storage.open()

        # TODO Here jenkins-task views come to play

        # tests
        last_build_id = storage['last_build_id']
        successes, failures, errors = [], [], []
        for build_id in xrange(1, last_build_id+1):
            build_data = storage['build-%d' % build_id]
            successes.append(build_data['tests-successes'])
            failures.append(build_data['tests-failures'])
            errors.append(build_data['tests-errors'])


        tests_chart = SimpleLineChart(400, 250)
        tests_chart.BASE_URL = 'http://chart.googleapis.com/chart?'
        # axis
        max_tests = max([s+f+e for s,f,e in zip(successes,failures,errors)])
        step = round(max_tests/10, 1-len(str(max_tests/10)))
        total_steps = math.ceil(1.0 * max_tests/step)
        tests_chart.set_axis_labels(Axis.LEFT, xrange(0, step*(total_steps+1), step))
        tests_chart.set_axis_labels(Axis.BOTTOM, xrange(1, last_build_id+1))
        tests_chart.set_grid(0, step/2, 5, 5)

        # First value - allowed maximum
        tests_chart.add_data([step*total_steps] * 2)
        # All tests, failures and errors, errors
        tests_chart.add_data([s+f+e for s,f,e in zip(successes,failures,errors)])
        tests_chart.add_data([f+e for f,e in zip(failures,errors)])
        tests_chart.add_data(errors)
        # Last value is the lowest in the Y axis.
        tests_chart.add_data([0] * 2)

        # Fill colors
        tests_chart.set_colours(['FFFFFF', '00FF00', 'FF0000', '0000FF'])
        tests_chart.add_fill_range('00FF00', 1, 2)
        tests_chart.add_fill_range('FF0000', 2, 3)
        tests_chart.add_fill_range('0000FF', 3, 4)

        # End jenkins-task views

        return render(request, 'django_jenkins/index.html',
                      { 'tests_chart' : tests_chart })
    finally:
        storage.close()

