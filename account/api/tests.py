import os, re, json

from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User

class SignUpTests(APITestCase):
    fixtures = []

    def get_confirmation_url_from_email(self, email_message):
        exp = r'(\/activate\/([a-z0-9\-]+)\/([a-z0-9\-]+))'
        m = re.search(exp, email_message)
        confirmation_url = m.group()
        user_uuid = m.group(2)
        confirmation_code = m.group(3)

        return confirmation_url, user_uuid, confirmation_code

    def test_sign_up(self):
        """
        Check that the sign up process works as expected
        """

        url = reverse('account-api:sign-up')

        data = {
            'full_name':'Ethan Sky Blue',
            'email':'test@test.com',
            'password':'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check confirmation email
        confirmation_email = str(mail.outbox[0].message())
        confirmation_url, user_uuid, confirmation_code = \
            self.get_confirmation_url_from_email(confirmation_email)

        # Get the API confirmation url
        url = reverse('account-public:activate', kwargs={
            'uuid':user_uuid, 'token':confirmation_code})

        response = self.client.get(url, HTTP_HOST=settings.SITE_DOMAIN)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(uuid=user_uuid)
        self.assertEquals(user.is_active, True)

    def test_sign_up_used_email(self):
        """
        Check that the user can't sign up with an email already used
        """

        url = reverse('account-api:sign-up')

        data = {
            'full_name':'Ethan Sky Blue',
            'email':'test@test.com',
            'password':'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'full_name':'Ethan Sky Blue',
            'email':'test@test.com',
            'password':'demo1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], ["This email is already used."])

    def test_sign_up_invalid_name(self):
        """
        Check that the full name is valid
        """

        url = reverse('account-api:sign-up')

        # Test full name too long

        data = {
            'full_name':'Too long too long too long too long too long Too long too long',
            'email':'test@test.com',
            'password':'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['full_name'], ["The full name must be 50 characters long maximum."])

        # Test full name too short

        data = {
            'full_name':'ab',
            'email':'test@test.com',
            'password':'demo1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['full_name'], ["The full name must be at least 3 characters long."])

        # Test full name invalid

        data = {
            'full_name':'ab $ 13',
            'email':'test@test.com',
            'password':'demo1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['full_name'], ["The full name field only accepts letters and hyphen."])

    def test_sign_up_invalid_email(self):
        """
        Check that the email is valid
        """

        url = reverse('account-api:sign-up')

        data = {
            'full_name':'Ethan Blue',
            'email':'test.test.com',
            'password':'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], ["This email address is not valid."])

    def test_sign_up_invalid_password(self):
        """
        Check that the password is valid
        """

        url = reverse('account-api:sign-up')

        # Test password too long

        data = {
            'full_name':'Ethan Blue',
            'email':'test@test.com',
            'password':'ToolongtoolongtoolongtoolongtoolongToolongtoolongToolongtoolong',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'], ["Password must be 50 characters long maximum."])

        # Test password too short

        data = {
            'full_name':'ab',
            'email':'test@test.com',
            'password':'demo1',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'], ["Password must be at least 6 characters long."])

    def test_sign_in(self):
        """
        Check that the sign in works after signing up
        """

        url = reverse('account-api:sign-up')

        data = {
            'full_name':'Ethan Sky Blue',
            'email':'test@test.com',
            'password':'demo1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('account-api:sign-in')

        data = {
            'email':'test@test.com',
            'password':'demo1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


