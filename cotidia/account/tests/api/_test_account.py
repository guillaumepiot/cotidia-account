import uuid
import json

from django.test import override_settings
from django.urls import reverse
from django.core import mail

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.renderers import JSONRenderer

from cotidia.account import fixtures
from cotidia.account.models import User
from cotidia.account.doc import Doc
from cotidia.account.tests.utils import (
    get_confirmation_url_from_email,
    get_reset_url_from_email
)


@override_settings(ACCOUNT_ENABLE_TWO_FACTOR=False)
class AccountAPITests(APITestCase):

    @fixtures.normal_user
    def setUp(self):
        self.doc = Doc()

        self.display_doc = True

    def jsonify(self, data):
        """Make clean JSON for doc output."""

        return json.loads(JSONRenderer().render(data).decode("utf-8"))

    def test_sign_up(self):
        """Check that the sign up process works as expected."""

        section_title = "Sign up"

        url = reverse('account-api:sign-up')

        data = {
            'full_name': 'Ethan Sky Blue',
            'email': 'test@test.com',
            'password': 'demo1234'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.filter().last()
        self.assertEqual(response.data['uuid'], str(user.uuid))

        if self.display_doc:
            # Generate documentation
            content = {
                'title': section_title,
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': self.jsonify(response.data),
            }
            self.doc.display_section(content)

        # Check confirmation email
        self.assertEqual(len(mail.outbox), 1)
        confirmation_email = str(mail.outbox[0].message())
        confirmation_url, user_uuid, confirmation_code = \
            get_confirmation_url_from_email(confirmation_email)

        # Get the API confirmation url
        url = reverse(
            'account-public:activate',
            kwargs={
                'uuid': user_uuid,
                'token': confirmation_code
            })

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(uuid=user_uuid)
        self.assertEquals(user.is_active, True)

    def test_sign_up_used_email(self):
        """Check that the user can't sign up with an email already used."""

        url = reverse('account-api:sign-up')

        data = {
            'full_name': 'Ethan Sky Blue',
            'email': 'test@test.com',
            'password': 'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'full_name': 'Ethan Sky Blue',
            'email': 'test@test.com',
            'password': 'demo1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['email'],
            ["This email is already used."]
        )

    def test_sign_up_invalid_name(self):
        """Check that the full name is valid."""

        url = reverse('account-api:sign-up')

        # Test full name too long

        data = {
            'full_name': 'Too long '*10,
            'email': 'test@test.com',
            'password': 'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['full_name'],
            ["The full name must be 50 characters long maximum."]
        )

        # Test full name too short

        data = {
            'full_name': 'ab',
            'email': 'test@test.com',
            'password': 'demo1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['full_name'],
            ["The full name must be at least 3 characters long."]
        )

        # Test full name invalid

        data = {
            'full_name': 'ab $ 13',
            'email': 'test@test.com',
            'password': 'demo1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['full_name'],
            [
                "The full name field only accepts letters, hyphen and "
                "apostrophe."
            ]
        )

    def test_sign_up_invalid_email(self):
        """Check that the email is valid."""

        url = reverse('account-api:sign-up')

        data = {
            'full_name': 'Ethan Blue',
            'email': 'test.test.com',
            'password': 'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['email'],
            ["This email address is not valid."]
        )

    def test_sign_up_invalid_password(self):
        """Check that the password is valid."""

        url = reverse('account-api:sign-up')

        # Test password too long

        data = {
            'full_name': 'Ethan Blue',
            'email': 'test@test.com',
            'password': 'Toolong' * 10,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['password'],
            ["Password must be 50 characters long maximum."]
        )

        # Test password too short

        data = {
            'full_name': 'ab',
            'email': 'test@test.com',
            'password': 'demo1',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['password'],
            ["Password must be at least 6 characters long."]
        )

    def test_sign_in(self):
        """Check that the sign in works after signing up."""

        section_title = "Sign in"

        url = reverse('account-api:sign-in')

        data = {
            'email': self.normal_user.email,
            'password': self.normal_user_pwd,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if self.display_doc:
            # Generate documentation
            content = {
                'title': section_title,
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': response.data
            }
            self.doc.display_section(content)

    def test_sign_up_one_name(self):
        """Check that the sign up works when user on submit one name."""

        url = reverse('account-api:sign-up')

        data = {
            'full_name': 'Ethan',
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
            'account-public:activate',
            kwargs={
                'uuid': user_uuid,
                'token': confirmation_code
            }
        )

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(uuid=user_uuid)
        self.assertEquals(user.is_active, True)

    def test_sign_up_mixed_case_email(self):
        """
        Test sign up with mixed case email.

        Check that the user can input a mixed case email, and that he can
        login with the same email, although it will be flatten in the database
        """

        url = reverse('account-api:sign-up')

        data = {
            'full_name': 'Ethan',
            'email': 'Test@test.com',
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
            'account-public:activate',
            kwargs={
                'uuid': user_uuid,
                'token': confirmation_code
            }
        )

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(uuid=user_uuid)
        self.assertEquals(user.is_active, True)

    def test_activate(self):
        """Test the various activation responses."""

        section_title = "Activate"
        description = (
            "The url should be formatted as follows:"
            "`/api/account/activate/<uuid>/<token>/`\n\n"
            "The activation API can return three activation statuses:\n\n"
            "- `USER_INVALID`\n"
            "- `TOKEN_INVALID`\n"
            "- `ACTIVATED`")

        url = reverse('account-api:sign-up')

        # Test validation (required field)

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

        self.assertEqual(confirmation_url, "/activate/{}/{}/".format(
            user_uuid,
            confirmation_code
        ))

        # Test invalid UUID
        url = reverse(
            'account-api:activate',
            kwargs={
                'uuid': uuid.uuid4(),
                'token': confirmation_code
            })
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "USER_INVALID")

        if self.display_doc:
            # Generate documentation
            content = {
                'title': "Activate with invalid user",
                'http_method': 'GET',
                'url': url,
                'payload': {
                    'uuid': str(uuid.uuid4()),
                    'token': '1234'
                },
                'response': self.jsonify(response.data),
                'description': description
            }
            self.doc.display_section(content)

        # Test invalid Token
        url = reverse(
            'account-api:activate',
            kwargs={
                'uuid': user_uuid,
                'token': '1234'
            })
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "TOKEN_INVALID")

        if self.display_doc:
            # Generate documentation
            content = {
                'title': "Activate with invalid token",
                'http_method': 'GET',
                'url': url,
                'payload': {
                    'uuid': str(user_uuid),
                    'token': '1234'
                },
                'response': self.jsonify(response.data),
                'description': description
            }
            self.doc.display_section(content)

        # Get the API confirmation url
        url = reverse(
            'account-api:activate',
            kwargs={
                'uuid': user_uuid,
                'token': confirmation_code
            })
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "ACTIVATED")

        user = User.objects.get(uuid=user_uuid)
        self.assertEquals(user.is_active, True)

        if self.display_doc:
            # Generate documentation
            content = {
                'title': section_title,
                'http_method': 'GET',
                'url': url,
                'payload': {
                    'uuid': str(user_uuid),
                    'token': confirmation_code
                },
                'response': self.jsonify(response.data),
                'description': description
            }
            self.doc.display_section(content)

    def test_activate_resend_link(self):
        """Test the various activation responses."""

        section_title = "Re-send activation link"
        description = ""

        url = reverse('account-api:sign-up')

        data = {
            'full_name': 'Ethan Sky Blue',
            'email': 'test@test.com',
            'password': 'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

        # Send the activaton link a second time
        user = User.objects.all().last()
        url = reverse(
            'account-api:resend-activation-link',
            kwargs={'uuid': str(user.uuid)}
        )
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(mail.outbox), 2)
        confirmation_email = str(mail.outbox[1].message())

        confirmation_url, user_uuid, confirmation_code = \
            get_confirmation_url_from_email(confirmation_email)

        self.assertEqual(confirmation_url, "/activate/{}/{}/".format(
            user_uuid,
            confirmation_code
        ))

        if self.display_doc:
            # Generate documentation
            content = {
                'title': section_title,
                'http_method': 'POST',
                'url': url,
                'payload': {},
                'response': self.jsonify(response.data),
                'description': description
            }
            self.doc.display_section(content)

        # Get the API confirmation url
        url = reverse(
            'account-api:activate',
            kwargs={
                'uuid': user_uuid,
                'token': confirmation_code
            })
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "ACTIVATED")

        user = User.objects.get(uuid=user_uuid)
        self.assertEquals(user.is_active, True)

    def test_authenticate(self):
        """Check that the authenticate works using the user uuid."""

        section_title = "Authenticate"

        url = reverse('account-api:sign-up')

        data = {
            'full_name': 'Ethan Sky Blue',
            'email': 'test@test.com',
            'password': 'demo1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        token = response.data['token']

        url = reverse('account-api:authenticate')

        # Invalid token
        data = {
            'token': '1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "TOKEN_INVALID")

        if self.display_doc:
            # Generate documentation
            content = {
                'title': "Authenticate with invalid token",
                'http_method': 'POST',
                'url': url,
                'payload': {
                    'token': '1234',
                },
                'response': self.jsonify(response.data)
            }
            self.doc.display_section(content)

        # Valid token
        data = {
            'token': token,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "USER_INACTIVE")

        if self.display_doc:
            # Generate documentation
            content = {
                'title': "Authenticate with inactive user",
                'http_method': 'POST',
                'url': url,
                'payload': {
                    'token': token,
                },
                'response': self.jsonify(response.data)
            }
            self.doc.display_section(content)

        # Activate user
        user = User.objects.filter().latest('id')
        user.is_active = True
        user.save()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if self.display_doc:
            # Generate documentation
            content = {
                'title': section_title,
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': response.data
            }
            self.doc.display_section(content)

    def test_reset_password(self):
        """Check that an email is sent with reset link."""

        section_title = "Reset password"

        data = {
            'email': self.normal_user.email
        }
        url = reverse('account-api:reset-password')
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.data['message'], "PASSWORD_RESET")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #
        # Check that an email is sent
        #
        self.assertEqual(len(mail.outbox), 1)

        if self.display_doc:
            # Generate documentation
            content = {
                'title': section_title,
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': response.data
            }
            self.doc.display_section(content)

        #
        # Test with an email that doesn't exists
        # It should still return OK to avoid people checking for email
        #
        data = {
            'email': 'inexistent@inexistent.com'
        }
        url = reverse('account-api:reset-password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_disabled_for_inactive_user(self):
        """The reset password API whouls be disabled for inactive users."""

        self.normal_user.is_active = False
        self.normal_user.save()

        data = {
            'email': self.normal_user.email
        }
        url = reverse('account-api:reset-password')
        response = self.client.post(url, data, format='json')
        self.assertEquals(
            response.data["non_field_errors"],
            ["Your account is not active."]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_uppercase_email(self):
        """
        Test reset with uppercase email.

        Check that if we submit and email with a different case, we still
        match the user.
        """

        data = {
            'email': self.normal_user.email.upper()
        }
        url = reverse('account-api:reset-password')
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.data['message'], "PASSWORD_RESET")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #
        # Check that an email is sent
        #
        self.assertEqual(len(mail.outbox), 1)

    def test_reset_key_valid(self):
        """Test that the reset key sent by email is valid."""

        section_title = "Validate reset token"

        description = (
            "The validate API can return two statuses:\n\n"
            "- `TOKEN_VALID`\n"
            "- `TOKEN_INVALID`")

        data = {
            'email': self.normal_user.email
        }
        url = reverse('account-api:reset-password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #
        # Check reset email
        #
        self.assertEqual(len(mail.outbox), 1)
        reset_email = str(mail.outbox[0].message())
        reset_url, user_uuid, reset_code = \
            get_reset_url_from_email(reset_email)

        #
        # Validate the reset code
        #
        url = reverse(
            'account-api:reset-password-validate',
            kwargs={
                'uuid': user_uuid,
                'token': reset_code
            })

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['message'], "TOKEN_VALID")

        if self.display_doc:
            # Generate documentation
            content = {
                'title': section_title,
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': self.jsonify(response.data),
                'description': description
            }
            self.doc.display_section(content)

        #
        # Test for TOKEN_INVALID status
        # Change the user password manually to force the token to be invalid
        #
        self.normal_user.set_password('Another')
        self.normal_user.save()

        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['message'], "TOKEN_INVALID")

        if self.display_doc:
            # Generate documentation
            content = {
                'title': "Reset key is invalid",
                'http_method': 'GET',
                'url': url,
                'payload': self.jsonify(data),
                'response': self.jsonify(response.data),
                'description': description
            }
            self.doc.display_section(content)

    def test_set_new_password(self):
        """Test that the user can set the new password."""

        section_title = "Set new password"

        description = (
            "The set password API can return two statuses:\n\n"
            "- `PASSWORD_SET`\n"
            "- `TOKEN_INVALID`")

        data = {
            'email': self.normal_user.email
        }
        url = reverse('account-api:reset-password')
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.data['message'], "PASSWORD_RESET")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #
        # Check reset email
        #
        self.assertEqual(len(mail.outbox), 1)
        reset_email = str(mail.outbox[0].message())
        reset_url, user_uuid, reset_code = \
            get_reset_url_from_email(reset_email)

        #
        # Validate the reset code with the set password url
        #
        url = reverse(
            'account-api:set-password',
            kwargs={
                'uuid': user_uuid,
                'token': reset_code
            })

        data = {
            'password1': "new password 123",
            'password2': "new password 123"
        }

        response = self.client.post(url, data)
        self.assertEquals(response.data['message'], "PASSWORD_SET")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        if self.display_doc:
            # Generate documentation
            content = {
                'title': section_title,
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': self.jsonify(response.data),
                'description': description
            }
            self.doc.display_section(content)

        #
        # Test for TOKEN_INVALID status
        # When we submit a second time, the token should invalid
        #

        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['message'], "TOKEN_INVALID")

        if self.display_doc:
            # Generate documentation
            content = {
                'title': "Reset password with invalid token",
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': self.jsonify(response.data),
                'description': description
            }
            self.doc.display_section(content)

        #
        # Test that the user can sign in with the new password
        #
        url = reverse('account-api:sign-in')

        data = {
            'email': self.normal_user.email,
            'password': 'new password 123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_valid(self):
        """Test that the password are valid and match."""

        data = {
            'email': self.normal_user.email
        }
        url = reverse('account-api:reset-password')
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.data['message'], "PASSWORD_RESET")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #
        # Check reset email
        #
        self.assertEqual(len(mail.outbox), 1)
        reset_email = str(mail.outbox[0].message())
        reset_url, user_uuid, reset_code = \
            get_reset_url_from_email(reset_email)

        #
        # That password mismatch
        #
        url = reverse(
            'account-api:set-password',
            kwargs={
                'uuid': user_uuid,
                'token': reset_code
            })

        data = {
            'password1': "demo1234",
            'password2': "demo4567"
        }

        response = self.client.post(url, data)
        self.assertEquals(
            response.data['non_field_errors'],
            ["The passwords didn't match."]
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        #
        # That password invalid
        #
        url = reverse(
            'account-api:set-password',
            kwargs={
                'uuid': user_uuid,
                'token': reset_code
            })

        data = {
            'password1': "demo",
            'password2': "demo"
        }

        response = self.client.post(url, data)
        self.assertEquals(
            response.data['password1'],
            ["The password is too short."]
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_details(self):
        """Test that details can be updated."""

        data = {
            'first_name': "Jack",
            'last_name': "Green",
            'email': "john@green.com"
        }
        url = reverse('account-api:update-details')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # With authentication
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['first_name'], "Jack")
        self.assertEquals(response.data['last_name'], "Green")
        self.assertEquals(response.data['email'], "john@green.com")

        if self.display_doc:
            # Generate documentation
            content = {
                'title': "Update details",
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': self.jsonify(response.data),
                'description': (
                    "Update the details of the user making the request."
                )
            }
            self.doc.display_section(content)

    def test_update_details_empty_values(self):
        """Test that details can be updated."""

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)

        data = {
            'first_name': "",
            'last_name': "",
            'email': ""
        }
        url = reverse('account-api:update-details')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data['first_name'], ['The first name may not be blank.'])
        self.assertEquals(
            response.data['last_name'], ['The last name may not be blank.'])
        self.assertEquals(
            response.data['email'], ['The email may not be blank.'])

        data = {}
        url = reverse('account-api:update-details')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data['first_name'], ['Please enter your first name.'])
        self.assertEquals(
            response.data['last_name'], ['Please enter your last name.'])
        self.assertEquals(
            response.data['email'], ['Please enter your email.'])

    def test_change_password(self):
        """Test that the user can change its password."""

        section_title = "Change password"

        url = reverse('account-api:change-password')

        data = {
            'current_password': self.normal_user_pwd,
            'password1': "another123",
            'password2': "another123"
        }

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key
        )

        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Check that the new password is set

        user = User.objects.get(id=self.normal_user.id)

        self.assertTrue(user.check_password("another123"))

        if self.display_doc:
            # Generate documentation
            content = {
                'title': section_title,
                'http_method': 'POST',
                'url': url,
                'payload': self.jsonify(data),
                'response': self.jsonify(response.data),
                'description': 'Change the user password.'
            }
            self.doc.display_section(content)

        # Test for invalid current password

        data = {
            'current_password': self.normal_user_pwd + "5",
            'password1': "another123",
            'password2': "another123"
        }

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key
        )

        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            response.data["current_password"],
            ["The current password is invalid."]
        )

    @override_settings(ACCOUNT_FORCE_ACTIVATION=False)
    def test_sign_up_no_activation(self):
        """Test sign up without activation email.

        If `ACCOUNT_FORCE_ACTIVATION` is set to False then the sign up
        call should create an active user and not send an activation
        email.
        """

        url = reverse('account-api:sign-up')

        data = {
            'full_name': 'Ethan Sky Blue',
            'email': 'test@test.com',
            'password': 'demo1234'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check confirmation email is not sent
        self.assertEqual(len(mail.outbox), 0)

        # Check that the user is active
        user = User.objects.filter().latest('id')
        self.assertEquals(user.is_active, True)
