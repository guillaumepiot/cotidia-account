from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import Permission

from cotidia.account import fixtures


class BaseAdminTestCase(TestCase):

    @fixtures.normal_user
    @fixtures.admin_user
    @fixtures.superuser
    def setUp(self):
        pass

    def check_page_permissions(self, namespace, urlname, permission, urlargs={}):
        """Check all access permissions for a given page."""

        if urlargs:
            url = reverse("{}:{}".format(namespace, urlname), kwargs=urlargs)
        else:
            url = reverse("{}:{}".format(namespace, urlname))

        response = self.client.get(url)
        self.assertEquals(response['Location'], '/admin/account/login/')
        self.assertEquals(response.status_code, 302)

        # Normal user
        self.client.login(
            username=self.normal_user.email,
            password=self.normal_user_pwd
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

        # Admin user without permission
        self.client.login(
            username=self.admin_user.email,
            password=self.admin_user_pwd
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 403)

        # Admin user with permission
        perm = Permission.objects.get(codename=permission)
        self.admin_user.user_permissions.add(perm)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

        # Superuser
        self.client.login(
            username=self.superuser.email,
            password=self.superuser_pwd
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
