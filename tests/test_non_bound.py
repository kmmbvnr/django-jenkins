from django.test import TestCase


class NonBoundTest(TestCase):
    def test_executed(self):
        """
        This test executed only if no --project-apps-tests option provided
        """
