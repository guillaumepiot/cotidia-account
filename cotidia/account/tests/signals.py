from mock import patch

from django.core.urlresolvers import reverse
from django.core import mail

from rest_framework import status
from rest_framework.test import APITestCase

from cotidia.account.tests.utils import get_confirmation_url_from_email


class AccountSignalsTests(APITestCase):

    @patch('cotidia.account.signals.user_activate')
    def test_user_activate_signal(self, mock):

        url = reverse('account-api:sign-up')
        data = {
            'full_name': 'Ethan Sky Blue',
            'email': 'test@test.com',
            'password': 'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check confirmation email
        confirmation_email = str(mail.outbox[0].message())
        confirmation_url, user_uuid, confirmation_code = \
            get_confirmation_url_from_email(confirmation_email)

        # Get the API confirmation url
        url = reverse(
            'account-api:activate',
            kwargs={
                'uuid': user_uuid,
                'token': confirmation_code
                })
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'ACTIVATED')

        # Check that your signal was called.
        self.assertTrue(mock.called)

        # Check that your signal was called only once.
        self.assertEqual(mock.call_count, 1)
