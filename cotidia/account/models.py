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
    NewUserActivationNotice,
    ResetPasswordNotice
    )


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

    def __str__(self):
        if self.first_name or self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        return self.username

    @property
    def token(self):
        token, created = Token.objects.get_or_create(user=self)
        return token

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

    def send_activation_link(self):
        """Create a new activation notice and send it straight away."""

        token = default_token_generator.make_token(self)

        if hasattr(settings, 'APP_URL'):
            APP_URL = settings.APP_URL
        else:
            APP_URL = settings.SITE_URL

        url = '{0}/activate/{1}/{2}/'.format(APP_URL, self.uuid, token)

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
