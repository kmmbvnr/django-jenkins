# -*- coding: utf-8 -*-
from django.dispatch import Signal

setup_test_environment = Signal()
teardown_test_environment = Signal()

before_suite_run = Signal()
after_suite_run = Signal()

build_suite = Signal(providing_args=["suite"])
