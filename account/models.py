import uuid
import types
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
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
        return reverse('account-admin:user_detail', kwargs={'slug': self.uuid})

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
        # Assign all the properties and attributes from user_model_definition to
        # the USer class.
        # Instance method are added using the types.MethodType mechanism,
        # pulling the method as straight function from the dict value of 
        # user_model_definition
        for field in user_model_definition.__dict__.keys():
            if not field.startswith('__'):
                # If the attribute is a instance method, then we need to bound
                # it to the class by decclaring it as MethodType. That way, it 
                # will accept self as first argument
                # Refer to: https://www.ianlewis.org/en/dynamically-adding-method-classes-or-class-instanc
                _type = type(getattr(user_model_definition, field))
                if _type is types.MethodType:
                    attrs[field] = types.MethodType(user_model_definition.__dict__[field], None, User)
                else:
                    attrs[field] = getattr(user_model_definition, field)


    # Create the new model class
    model_class = type('User', (User,), attrs)


    return model_class




if hasattr(settings, 'ACCOUNT_USER_MODEL'):
    CustomUser = import_model(settings.ACCOUNT_USER_MODEL, "User")
    User = build_user_model(CustomUser)
else:
    User = build_user_model()
