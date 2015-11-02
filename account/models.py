import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .utils import import_model


class BaseUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        if self.first_name or self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'uuid': self.uuid})

    class Meta:
        abstract = True

if hasattr(settings, 'ACCOUNT_USER_MODEL'):

    cls = import_model(settings.ACCOUNT_USER_MODEL, "User")

    class User(cls):
        pass

else:
    class User(BaseUser):
        pass