from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

from cotidia.account.models import User


@receiver(post_save, sender=User)
def user_update(sender, instance, created, **kwargs):
    pass

# Account registraton signals
# user_sign_up = Signal(providing_args=["request", "user"])
# user_sign_in = Signal(providing_args=["request", "user"])
user_activate = Signal(providing_args=["request", "user"])
# user_authenticate = Signal(providing_args=["request", "user"])
# user_set_password = Signal(providing_args=["request", "user"])


@receiver(user_activate)
def user_activate_update(sender, request, user, **kwargs):
    """Call upon `user_activate` signal sent."""
    pass
