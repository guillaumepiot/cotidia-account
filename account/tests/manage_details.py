import re

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.contrib.sites.models import Site

from account.models import User

class ManageDetailsTest(TestCase):

    def setUp(self):
        pass


    def test_change_password(self):
        # Login
        """
        Test POST on /account/login/
        """
        data = {
            'username':'test@test.com',
            'password':'demo1234',
        }
        response = self.client.post(reverse("account_login"), data, HTTP_HOST=self.HTTP_HOST)
        self.assertEquals(response.status_code, 302)

        # Change password
        data = {
            'old_password':'demo1234',
            'new_password1':'demo123',
            'new_password2':'demo123',
        }
        response = self.client.post(reverse("account_password_change"), data, HTTP_HOST=self.HTTP_HOST)
        # Should not redirect as not allowed to login
        self.assertEquals(response.status_code, 302)


    def test_update_details(self):

        data = {
            'username':'test@test.com',
            'password':'demo1234',
        }
        response = self.client.post(reverse("account_login"), data, HTTP_HOST=self.HTTP_HOST)
        self.assertEquals(response.status_code, 302)

        data = {
            'title':'mr',
            'first_name':'John',
            'last_name':'Johnson',
            'email':'test@test.com',
            'company_name':'companyabc',
            'phone_number':'08233114343',
            'mobile_number':'0763362743',
            'fax_number':'712037123',
        }
        response = self.client.post(reverse("account_update_details"), data, HTTP_HOST=self.HTTP_HOST)
        # Should not redirect as not allowed to login
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '%s%s%s' % (self.PROTOCOL, self.HTTP_HOST, reverse("my_account")))
        