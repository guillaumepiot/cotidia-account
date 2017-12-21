import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from cotidia.account.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from rest_framework.authtoken.models import Token
from two_factor.utils import default_device

from cotidia.account.notices import (
    NewUserActivationNotice
)
from cotidia.account.managers import UserManager


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(
        _('email address'),
        blank=True,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    objects = UserManager()

    # Used in createsuperuser manage command
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        if self.first_name or self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        return self.username

    @property
    def token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def has_password(self):
        if self.password:
            return True
        else:
            return False

    @property
    def two_factor_auth_enabled(self):
        if self.is_staff or self.is_superuser:
            return default_device(self)
        return False

    def get_absolute_url(self):
        """Create the absolute url to the admin user detail view."""
        return reverse('account-admin:user_detail', kwargs={'slug': self.uuid})

    def send_activation_link(self, app=False):
        """Create a new activation notice and send it straight away."""

        token = default_token_generator.make_token(self)

        if app is True and hasattr(settings, "APP_URL"):
            url = '{0}/activate/{1}/{2}/'.format(
                settings.APP_URL, self.uuid, token)
        else:
            url = '{0}{1}'.format(
                settings.SITE_URL,
                reverse('account-public:activate', kwargs={
                    'uuid': self.uuid,
                    'token': token
                })
            )

        notice = NewUserActivationNotice(
            recipients=['{0} <{1}>'.format(
                self.get_full_name(), self.email
            )],
            context={
                'url': url,
                'first_name': self.first_name
            }
        )
        notice.send(force_now=True)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
