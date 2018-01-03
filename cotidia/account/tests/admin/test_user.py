from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, Permission

from cotidia.account.models import User
from cotidia.account.factory import UserFactory
from cotidia.account.tests.admin.utils import BaseAdminTestCase


class UserAdminTests(BaseAdminTestCase):

    def test_user_add(self):
        """Test we can add a user."""

        self.check_page_permissions('account-admin', 'user-add', 'add_user')

        # Test with minimum data
        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
        }

        response = self.client.post(reverse('account-admin:user-add'), data)
        self.assertEquals(response.status_code, 302)

        # Test with all data
        group = Group.objects.create(name="Test group")
        perm = Permission.objects.get(codename="add_user")

        data = {
            'first_name': "Frank",
            'last_name': "Green",
            'email': 'test2@test.com',
            'username': 'test2@test.com',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
            'groups': [group.id],
            'user_permissions': [perm.id]
        }

        response = self.client.post(reverse('account-admin:user-add'), data)
        self.assertEquals(response.status_code, 302)

        user = User.objects.filter().latest('id')
        self.assertEquals(user.first_name, data['first_name'])
        self.assertEquals(user.last_name, data['last_name'])
        self.assertEquals(user.email, data['email'])
        self.assertEquals(user.username, data['username'])
        self.assertEquals(user.is_active, data['is_active'])
        self.assertEquals(user.is_staff, data['is_staff'])
        self.assertEquals(user.is_superuser, data['is_superuser'])
        self.assertEquals(
            [g.id for g in user.groups.all()],
            data['groups']
        )
        self.assertEquals(
            [p.id for p in user.user_permissions.all()],
            data['user_permissions']
        )

    def test_user_get_invitation_if_active(self):
        """Test the new active user receives an invitation email."""

        self.client.login(
            username=self.superuser.email,
            password=self.superuser_pwd
        )

        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
            'is_active': True,
        }

        response = self.client.post(reverse('account-admin:user-add'), data)
        self.assertEquals(response.status_code, 302)

        # Check that mail is sent
        self.assertEquals(len(mail.outbox), 1)

    def test_user_no_invitation_if_not_active(self):
        """Test the new inactive user doesn't get an invitation email."""

        self.client.login(
            username=self.superuser.email,
            password=self.superuser_pwd
        )

        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
            'is_active': False,
        }

        response = self.client.post(reverse('account-admin:user-add'), data)
        self.assertEquals(response.status_code, 302)

        # Check that mail is sent
        self.assertEquals(len(mail.outbox), 0)

    def test_user_add_inactive_update_active(self):
        """Test the change of user active.

        When we first create the user, it is inactive and receives no email.
        Then, we make them active, sending the invitation email.
        Finally, when they are active, they should not receive the email again.
        """

        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
            'is_active': False,
        }

        user = UserFactory.create(**data)

        urlargs = {'pk': user.pk}
        self.check_page_permissions('account-admin', 'user-update', 'change_user', urlargs)

        self.client.login(
            username=self.superuser.email,
            password=self.superuser_pwd
        )

        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
            'is_active': True,
        }

        response = self.client.post(
            reverse('account-admin:user-update', kwargs={'pk': user.pk}),
            data
        )
        self.assertEquals(response.status_code, 302)

        # Check that mail is sent
        # self.assertEquals(len(mail.outbox), 1)

        user = User.objects.filter().latest('id')
        self.assertEquals(user.is_active, True)
        self.assertEquals(user.is_staff, False)

        # User sets the password
        user.set_password('1234')
        user.save()

        # If the user has a password, no need to send the invitation email

        mail.outbox = []

        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
            'is_active': True,
        }

        response = self.client.post(
            reverse('account-admin:user-update', kwargs={'pk': user.pk}),
            data
        )
        self.assertEquals(response.status_code, 302)

        # Check that mail is sent
        self.assertEquals(len(mail.outbox), 0)

        # Make user inactive
        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
            'is_active': False,
        }

        response = self.client.post(
            reverse('account-admin:user-update', kwargs={'pk': user.pk}),
            data
        )
        self.assertEquals(response.status_code, 302)

        user = User.objects.filter().latest('id')
        self.assertEquals(user.is_active, False)
        self.assertEquals(user.is_staff, False)

        # Now the user already have a password, so making it active shouldn't
        # trigger the invitation email.

        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
            'is_active': True,
        }

        response = self.client.post(
            reverse('account-admin:user-update', kwargs={'pk': user.pk}),
            data
        )
        self.assertEquals(response.status_code, 302)

        # Check that mail is sent
        self.assertEquals(len(mail.outbox), 0)

    def test_user_invite_manually(self):
        """Test that an admin can re-send an invitation email."""

        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
            'is_active': True,
        }

        user = UserFactory.create(**data)

        urlargs = {'pk': user.pk}
        self.check_page_permissions('account-admin', 'user-invite', 'change_user', urlargs)

        self.client.login(
            username=self.superuser.email,
            password=self.superuser_pwd
        )

        response = self.client.post(
            reverse('account-admin:user-invite', kwargs={'pk': user.pk}),
            {}
        )

        self.assertEquals(response.status_code, 302)

        # Check that mail is sent
        self.assertEquals(len(mail.outbox), 1)
