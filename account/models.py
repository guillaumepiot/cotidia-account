import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .utils import import_model

from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        if self.first_name or self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'uuid': self.uuid})

    class Meta:
        abstract = True


def build_user_model(user_model_definition=None):
    """ 
    Create a custom (dynamic) model class based on the given definition.
    """

    # We'll build the class attributes here
    attrs = {}
    attrs['__module__'] = 'account.models'

    class Meta:
        app_label = 'account'
        abstract = False
    
    attrs['Meta'] = Meta

    if user_model_definition:
        # All of that was just getting the class ready, here is the magic
        # Build your model by adding django database Field subclasses to the attrs dict
        # What this looks like depends on how you store the users's definitions
        # For now, I'll just make them all CharFields
        for field in user_model_definition.__dict__.keys():
            if not field.startswith('__'):
                attrs[field] = getattr(user_model_definition, field)


    # Create the new model class
    model_class = type('User', (User,), attrs)

    return model_class




if hasattr(settings, 'ACCOUNT_USER_MODEL'):
    CustomUser = import_model(settings.ACCOUNT_USER_MODEL, "User")
    User = build_user_model(CustomUser)
else:
    User = build_user_model()
