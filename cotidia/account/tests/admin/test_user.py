from django.core import mail
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import Group, Permission

from cotidia.account import fixtures
from cotidia.account.models import User
from cotidia.account.factory import UserFactory


class UserAdminTests(TestCase):

    @fixtures.normal_user
    @fixtures.admin_user
    @fixtures.superuser
    def setUp(self):

        # Create a new group
        self.test_group = Group.objects.create(name="Test group")
        # Get the add user permission
        self.test_add_user_perm = Permission.objects.get(codename="add_user")
        self.test_change_user_perm = Permission.objects.get(codename="change_user")
        self.test_delete_user_perm = Permission.objects.get(codename="delete_user")

        self.test_users = {
            'superuser': UserFactory.create(
                first_name="Super",
                last_name="User",
                email='jack@user.com',
                username='jack@user.com',
                is_active=True,
                is_staff=True,
                is_superuser=True
            ),
            'staff': UserFactory.create(
                first_name="Staff",
                last_name="User",
                email='staff@user.com',
                username='staff@user.com',
                is_active=True,
                is_staff=True,
                is_superuser=False
            ),
            'normal': UserFactory.create(
                first_name="Normal",
                last_name="User",
                email='normal@user.com',
                username='normal@user.com',
                is_active=True,
                is_staff=False,
                is_superuser=False
            )
        }

        self.test_users['staff'].groups.add(self.test_group)
        self.test_users['staff'].user_permissions.add(self.test_add_user_perm)
        self.test_users['staff'].user_permissions.add(self.test_change_user_perm)
        self.test_users['staff'].user_permissions.add(self.test_delete_user_perm)

        self.data_full = {
            'first_name': "Jack",
            'last_name': "Red",
            'email': 'jack@red.com',
            'username': 'jack@red.com',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
            'groups': [self.test_group.id],
            'user_permissions': [self.test_change_user_perm.id]
        }

        # The results we expect to get if a staff user change another staff
        self.expected_results_partial = {
            'first_name': "Jack",
            'last_name': "Red",
            'email': 'jack@red.com',
            'username': 'jack@red.com',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'groups': [],
            'user_permissions': []
        }

    def as_superuser(self):
        self.client.login(
            username=self.superuser.email,
            password=self.superuser_pwd
        )
        self.user_level = 'superuser'

    def as_staff(self):
        self.client.login(
            username=self.admin_user.email,
            password=self.admin_user_pwd
        )
        self.admin_user.user_permissions.add(self.test_add_user_perm)
        self.admin_user.user_permissions.add(self.test_change_user_perm)
        self.admin_user.user_permissions.add(self.test_delete_user_perm)
        self.user_level = 'staff'

    def as_normal(self):
        self.client.login(
            username=self.normal_user.email,
            password=self.normal_user_pwd
        )
        self.user_level = 'normal'

    def assess_list_normal(self, status_code):

        url = reverse('account-admin:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def assess_list_admin(self, status_code):

        url = reverse('account-admin:user-list-admin')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def assess_add_get(self, status_code):

        url = reverse('account-admin:user-add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def assess_add_post(self, status_code):

        url = reverse('account-admin:user-add')
        data = self.data_full.copy()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status_code)

        if status_code == 302:
            values_tested = False
            obj = User.objects.latest('id')

            if self.user_level == 'superuser':

                # A superuser can update all the fields for any user.
                # Therefore all post data should be applied.

                self.assertEqual(obj.first_name, self.data_full['first_name'])
                self.assertEqual(obj.last_name, self.data_full['last_name'])
                self.assertEqual(obj.email, self.data_full['email'])
                self.assertEqual(obj.username, self.data_full['username'])
                self.assertEqual(obj.is_active, self.data_full['is_active'])
                self.assertEqual(obj.is_staff, self.data_full['is_staff'])
                self.assertEqual(obj.is_superuser, self.data_full['is_superuser'])
                self.assertEqual([g.id for g in obj.groups.all()], self.data_full['groups'])
                self.assertEqual([u.id for u in obj.user_permissions.all()], self.data_full['user_permissions'])
                values_tested = True

            elif self.user_level == 'staff':

                # A staff user can not promote a user to staff or superuser,
                # and can not assign groups or permission.
                # Therefore only partial post data should be applied.

                self.assertEqual(obj.first_name, self.expected_results_partial['first_name'])
                self.assertEqual(obj.last_name, self.expected_results_partial['last_name'])
                self.assertEqual(obj.email, self.expected_results_partial['email'])
                self.assertEqual(obj.username, self.expected_results_partial['username'])
                self.assertEqual(obj.is_active, self.expected_results_partial['is_active'])
                self.assertEqual(obj.is_staff, self.expected_results_partial['is_staff'])
                self.assertEqual(obj.is_superuser, self.expected_results_partial['is_superuser'])
                self.assertEqual(list(obj.groups.all()), self.expected_results_partial['groups'])
                self.assertEqual(list(obj.user_permissions.all()), self.expected_results_partial['user_permissions'])
                values_tested = True

            self.assertTrue(values_tested)

    def assess_detail_get(self, status_code, user_type):

        obj = self.test_users[user_type]

        url = reverse('account-admin:user-detail', kwargs={'pk': obj.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def assess_update_get(self, status_code, user_type):

        obj = self.test_users[user_type]

        url = reverse('account-admin:user-update', kwargs={'pk': obj.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def assess_update_post(self, status_code, user_type):

        obj = self.test_users[user_type]

        url = reverse('account-admin:user-update', kwargs={'pk': obj.id})
        data = self.data_full.copy()
        response = self.client.post(url, data)

        if response.status_code == 200:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, status_code)

        if status_code == 302:
            values_tested = False
            obj.refresh_from_db()

            if self.user_level == 'superuser':

                # A superuser can update all the fields for any user.
                # Therefore all post data should be applied.

                self.assertEqual(obj.first_name, self.data_full['first_name'])
                self.assertEqual(obj.last_name, self.data_full['last_name'])
                self.assertEqual(obj.email, self.data_full['email'])
                self.assertEqual(obj.username, self.data_full['username'])
                self.assertEqual(obj.is_active, self.data_full['is_active'])
                self.assertEqual(obj.is_staff, self.data_full['is_staff'])
                self.assertEqual(obj.is_superuser, self.data_full['is_superuser'])
                self.assertEqual([g.id for g in obj.groups.all()], self.data_full['groups'])
                self.assertEqual([u.id for u in obj.user_permissions.all()], self.data_full['user_permissions'])
                values_tested = True

            elif self.user_level == 'staff':

                # A staff user can not promote a user to staff or superuser,
                # and can not assign groups or permission.
                # Therefore only partial post data should be applied.

                self.assertEqual(obj.first_name, self.expected_results_partial['first_name'])
                self.assertEqual(obj.last_name, self.expected_results_partial['last_name'])
                self.assertEqual(obj.email, self.expected_results_partial['email'])
                self.assertEqual(obj.username, self.expected_results_partial['username'])
                self.assertEqual(obj.is_active, self.expected_results_partial['is_active'])
                self.assertEqual(obj.is_staff, self.expected_results_partial['is_staff'])
                self.assertEqual(obj.is_superuser, self.expected_results_partial['is_superuser'])
                self.assertEqual(list(obj.groups.all()), self.expected_results_partial['groups'])
                self.assertEqual(list(obj.user_permissions.all()), self.expected_results_partial['user_permissions'])
                values_tested = True

            self.assertTrue(values_tested)

    def assess_delete_get(self, status_code, user_type):

        obj = self.test_users[user_type]

        url = reverse('account-admin:user-delete', kwargs={'pk': obj.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def assess_delete_post(self, status_code, user_type):

        obj = self.test_users[user_type]

        url = reverse('account-admin:user-delete', kwargs={'pk': obj.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status_code)

    def assess_change_password_get(self, status_code, user_type):

        obj = self.test_users[user_type]

        url = reverse('account-admin:user-change-password', kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def assess_change_password_post(self, status_code, user_type):

        obj = self.test_users[user_type]

        url = reverse('account-admin:user-change-password', kwargs={'pk': obj.pk})

        data = {
            'password1': 'demo1234',
            'password2': 'demo1234',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status_code)

    def assess_invite_get(self, status_code, user_type):

        obj = self.test_users[user_type]

        url = reverse('account-admin:user-invite', kwargs={'pk': obj.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def assess_invite_post(self, status_code, user_type):

        obj = self.test_users[user_type]

        url = reverse('account-admin:user-invite', kwargs={'pk': obj.pk})

        response = self.client.post(url)

        self.assertEquals(response.status_code, status_code)

        # Check that mail is sent
        if status_code == 302:
            self.assertEquals(len(mail.outbox), 1)

    # Superuser tests

    def test_superuser_list_normal(self):
        self.as_superuser()
        self.assess_list_normal(200)

    def test_superuser_list_admin(self):
        self.as_superuser()
        self.assess_list_admin(200)

    def test_superuser_add(self):
        self.as_superuser()
        self.assess_add_get(200)
        self.assess_add_post(302)

    def test_superuser_detail(self):
        self.as_superuser()
        self.assess_detail_get(200, 'superuser')
        self.assess_detail_get(200, 'staff')
        self.assess_detail_get(200, 'normal')

    def test_superuser_update_superuser(self):
        self.as_superuser()
        self.assess_update_get(200, 'superuser')
        self.assess_update_post(302, 'superuser')

    def test_superuser_update_staff(self):
        self.as_superuser()
        self.assess_update_get(200, 'staff')
        self.assess_update_post(302, 'staff')

    def test_superuser_update_normal(self):
        self.as_superuser()
        self.assess_update_get(200, 'normal')
        self.assess_update_post(302, 'normal')

    def test_superuser_delete(self):
        self.as_superuser()
        self.assess_delete_get(200, 'superuser')
        self.assess_delete_get(200, 'staff')
        self.assess_delete_get(200, 'normal')
        self.assess_delete_post(302, 'superuser')
        self.assess_delete_post(302, 'staff')
        self.assess_delete_post(302, 'normal')

    def test_superuser_change_password(self):
        self.as_superuser()
        self.assess_change_password_get(200, 'superuser')
        self.assess_change_password_get(200, 'staff')
        self.assess_change_password_get(200, 'normal')
        self.assess_change_password_post(302, 'superuser')
        self.assess_change_password_post(302, 'staff')
        self.assess_change_password_post(302, 'normal')

    def test_superuser_invite_superuser(self):
        self.as_superuser()
        self.assess_invite_get(200, 'superuser')
        self.assess_invite_post(302, 'superuser')

    def test_superuser_invite_staff(self):
        self.as_superuser()
        self.assess_invite_get(200, 'staff')
        self.assess_invite_post(302, 'staff')

    def test_superuser_invite_normal(self):
        self.as_superuser()
        self.assess_invite_get(200, 'normal')
        self.assess_invite_post(302, 'normal')

    # Staff tests

    def test_staff_list_normal(self):
        self.as_staff()
        self.assess_list_normal(200)

    def test_staff_list_admin(self):
        self.as_staff()
        self.assess_list_admin(403)

    def test_staff_add(self):
        self.as_staff()
        self.assess_add_get(200)
        self.assess_add_post(302)

    def test_staff_detail(self):
        self.as_staff()
        self.assess_detail_get(403, 'superuser')
        self.assess_detail_get(403, 'staff')
        self.assess_detail_get(200, 'normal')

    def test_staff_update_superuser(self):
        self.as_staff()
        self.assess_update_get(403, 'superuser')
        self.assess_update_post(403, 'superuser')

    def test_staff_update_staff(self):
        self.as_staff()
        self.assess_update_get(403, 'staff')
        self.assess_update_post(403, 'staff')

    def test_staff_update_normal(self):
        self.as_staff()
        self.assess_update_get(200, 'normal')
        self.assess_update_post(302, 'normal')

    def test_staff_delete(self):
        self.as_staff()
        self.assess_delete_get(403, 'superuser')
        self.assess_delete_get(403, 'staff')
        self.assess_delete_get(200, 'normal')
        self.assess_delete_post(403, 'superuser')
        self.assess_delete_post(403, 'staff')
        self.assess_delete_post(302, 'normal')

    def test_staff_change_password(self):
        self.as_staff()
        self.assess_change_password_get(403, 'superuser')
        self.assess_change_password_get(403, 'staff')
        self.assess_change_password_get(200, 'normal')
        self.assess_change_password_post(403, 'superuser')
        self.assess_change_password_post(403, 'staff')
        self.assess_change_password_post(302, 'normal')

    def test_staff_invite(self):
        self.as_staff()
        self.assess_invite_get(403, 'superuser')
        self.assess_invite_get(403, 'staff')
        self.assess_invite_get(200, 'normal')
        self.assess_invite_post(403, 'superuser')
        self.assess_invite_post(403, 'staff')
        self.assess_invite_post(302, 'normal')

    # Normal tests

    def test_normal_list_normal(self):
        self.as_normal()
        self.assess_list_normal(403)

    def test_normal_list_admin(self):
        self.as_normal()
        self.assess_list_admin(403)

    def test_normal_add(self):
        self.as_normal()
        self.assess_add_get(403)
        self.assess_add_post(403)

    def test_normal_detail(self):
        self.as_normal()
        self.assess_detail_get(403, 'superuser')
        self.assess_detail_get(403, 'staff')
        self.assess_detail_get(403, 'normal')

    def test_normal_update(self):
        self.as_normal()
        self.assess_update_get(403, 'superuser')
        self.assess_update_get(403, 'staff')
        self.assess_update_get(403, 'normal')
        self.assess_update_post(403, 'superuser')
        self.assess_update_post(403, 'staff')
        self.assess_update_post(403, 'normal')

    def test_normal_delete(self):
        self.as_normal()
        self.assess_delete_get(403, 'superuser')
        self.assess_delete_get(403, 'staff')
        self.assess_delete_get(403, 'normal')
        self.assess_delete_post(403, 'superuser')
        self.assess_delete_post(403, 'staff')
        self.assess_delete_post(403, 'normal')

    def test_normal_change_password(self):
        self.as_normal()
        self.assess_change_password_get(403, 'superuser')
        self.assess_change_password_get(403, 'staff')
        self.assess_change_password_get(403, 'normal')
        self.assess_change_password_post(403, 'superuser')
        self.assess_change_password_post(403, 'staff')
        self.assess_change_password_post(403, 'normal')

    def test_normal_invite(self):
        self.as_normal()
        self.assess_invite_get(403, 'superuser')
        self.assess_invite_get(403, 'staff')
        self.assess_invite_get(403, 'normal')
        self.assess_invite_post(403, 'superuser')
        self.assess_invite_post(403, 'staff')
        self.assess_invite_post(403, 'normal')
