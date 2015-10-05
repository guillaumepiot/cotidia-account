import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        if self.first_name or self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'uuid': self.uuid})