import re

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from account.models import User

class SignUpTest(TestCase):

    def setUp(self):
       pass

    def get_confirmation_url_from_email(self, email_message):
        site_url = settings.SITE_URL.replace('/', '\/')
        exp = r'('+site_url+'\/([a-z\-\/]+)?account\/activate\/(.*)\/)'
        m = re.search(exp, email_message)
        confirmation_url = m.group()
        confirmation_code = m.group(2)

        return confirmation_url

    def test_signup_view(self):
        """
        Test GET on /account/sign-up/
        """
        response = self.client.get(reverse("account-public:sign-up"))
        self.assertEquals(response.status_code, 200)

    def test_signup_submit(self):
        """
        Test POST on /account/sign-up/
        """
        data = {
            'email':'test@test.com',
            'password1':'demo123',
            'password2':'demo123',
        }
        response = self.client.post(reverse("account-public:sign-up"), data)
        self.assertEquals(response.status_code, 302)

        # test login no confirm
        """
        Test POST on /account/login/
        """
        data = {
            'username':'test@test.com',
            'password':'demo123',
        }
        response = self.client.post(reverse("account-public:login"), data)
        # Should not redirect as not allowed to login
        self.assertEquals(response.status_code, 302)

    def test_signup_and_confirm_with_email(self):
        """
        Test POST on /account/sign-up/
        """
        data = {
            'email':'test@test.com',
            'password1':'demo123',
            'password2':'demo123',
        }
        response = self.client.post(reverse("account-public:sign-up"), data)
        self.assertEquals(response.status_code, 302)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Sign up confirmation')

        email_message = str(mail.outbox[0].message())
        confirmation_url = self.get_confirmation_url_from_email(email_message)

        response = self.client.get(confirmation_url)
        self.assertEquals(response.status_code, 200)

        # Test login
        """
        Test POST on /account/login/
        """
        data = {
            'username':'test@test.com',
            'password':'demo123',
        }
        response = self.client.post(reverse("account-public:login"), data)
        self.assertEquals(response.status_code, 302)

        # test logout
        response = self.client.post(reverse("account-public:logout"), data)
        self.assertEquals(response.status_code, 200)

    
    def test_password_reset(self):

        data = {
            'email':'test@test.com',
            'password1':'demo123',
            'password2':'demo123',
        }
        response = self.client.post(reverse("account-public:sign-up"), data)
        self.assertEquals(response.status_code, 302)

        # Confirm the account
        email_message = str(mail.outbox[0].message())
        confirmation_url = self.get_confirmation_url_from_email(email_message)

        response = self.client.get(confirmation_url)
        self.assertEquals(response.status_code, 200)

        # Clear the mailbox
        mail.outbox = []

        # Reset the password
        data = {
            'email':'test@test.com',
        }
        response = self.client.post(reverse("account-public:password_reset"), data)
        self.assertEquals(response.status_code, 302)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Password reset')

        email_message = str(mail.outbox[0].message())

        site_url = settings.SITE_URL.replace('/', '\/')
        exp = r'('+site_url+'\/([a-z\-\/]+)?account\/password\/reset\/confirm\/([a-zA-Z0-9\-]+)\/)'
        
        m = re.search(exp, email_message)
        reset_url = m.group()

        # Reset the password using that url
        data = {
            'new_password1':'demo1234',
            'new_password2':'demo1234',
        }
        response = self.client.post(reset_url, data)
        self.assertEquals(response.status_code, 302)



        
