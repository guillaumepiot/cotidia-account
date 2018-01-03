from django.core.urlresolvers import reverse

from cotidia.account.models import User
from cotidia.account.factory import UserFactory
from cotidia.account.tests.admin.utils import BaseAdminTestCase
from cotidia.account.tests.profile.models import Profile


class ProfileAdminTests(BaseAdminTestCase):

    def test_profile_add(self):
        """Test we can add a profile."""

        # Test with minimum data
        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
        }

        user = UserFactory.create(**data)

        urlargs = {'user_id': user.id}
        self.check_page_permissions('profile-admin', 'profile-add', 'add_profile', urlargs)

        response = self.client.get(reverse('profile-admin:profile-add', kwargs=urlargs))
        self.assertEquals(response.status_code, 200)

        data = {
            'company': "Cotidia"
        }

        response = self.client.post(reverse('profile-admin:profile-add', kwargs=urlargs), data)
        self.assertEquals(response.status_code, 302)

        user = User.objects.filter().latest('id')
        self.assertEquals(user.profile.company, data['company'])

    def test_profile_update(self):
        """Test we can update a profile."""

        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
        }

        user = UserFactory.create(**data)
        profile = Profile.objects.create(user=user, company="Cotidia")

        urlargs = {'pk': profile.id}
        self.check_page_permissions('profile-admin', 'profile-update', 'change_profile', urlargs)

        data = {
            'company': "Another company"
        }

        response = self.client.post(
            reverse('profile-admin:profile-update', kwargs={'pk': profile.id}),
            data
        )
        self.assertEquals(response.status_code, 302)

        user = User.objects.filter().latest('id')
        self.assertEquals(user.profile.company, data['company'])

    def test_profile_delete(self):
        """Test we can delete a profile."""

        data = {
            'email': 'test@test.com',
            'username': 'test@test.com',
        }

        user = UserFactory.create(**data)
        profile = Profile.objects.create(user=user, company="Cotidia")

        urlargs = {'pk': profile.id}
        self.check_page_permissions('profile-admin', 'profile-delete', 'delete_profile', urlargs=urlargs)

        response = self.client.post(
            reverse('profile-admin:profile-delete', kwargs=urlargs),
            data
        )
        self.assertEquals(response.status_code, 302)

        user = User.objects.filter().latest('id')
        self.assertEquals(hasattr(user, 'profile'), False)
