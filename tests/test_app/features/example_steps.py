# -*- coding: utf-8 -*-
from lettuce import step, before

@before.each_scenario
def setup_scenario(scenario):
    scenario.numbers = []

@step(u'(?:Given|And|When) the number "(.*)"(?: is added to (?:it|them))?')
def given_the_number(step, number):
    step.scenario.numbers.append(int(number))

@step(u'Then the result should be "(.*)"')
def then_the_result_should_equal(step, result):
    actual = sum(step.scenario.numbers)
    assert int(result) == actual, "%s != %s" % (result, actual)
