# -*- coding: utf-8 -*-
from django.dispatch import Signal

setup_test_environment = Signal()
teardown_test_environment = Signal()

before_suite_run = Signal()
after_suite_run = Signal()

build_suite = Signal(providing_args=["suite"])

test_add_failure = Signal(providing_args=['test', 'err'])
test_add_error = Signal(providing_args=['test', 'err'])
test_add_success = Signal(providing_args=['test'])

