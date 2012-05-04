from django.core import mail
from django.test import TestCase
from django.utils.unittest import skip


class SaintyChecks(TestCase):
    def test_mailbox_stubs_not_broken(self):
        print "Testing mailbox django stubs"
        mail.send_mail('Test subject', 'Test message', 'nobody@kenkins.com',
                       ['somewhere@nowhere.com'])
        self.assertTrue(1, len(mail.outbox))

    @skip("Check skiped test")
    def test_is_skipped(self):
        print "This test should be skipped"

    #def test_failure(self):
    #    raise Exception("Ups, should be disabled")

