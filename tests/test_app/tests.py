from django.core import mail
from django.test import TestCase


class SaintyChecks(TestCase):
    def test_mailbox_stubs_not_broken(self):
        mail.send_mail('Test subject', 'Test message', 'nobody@kenkins.com',
                       ['somewhere@nowhere.com'])
        self.assertTrue(1, len(mail.outbox))

