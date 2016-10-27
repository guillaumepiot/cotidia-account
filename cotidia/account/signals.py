from django.dispatch import receiver
from django.db.models.signals import post_save

from cotidia.account.models import User


@receiver(post_save, sender=User)
def user_update(sender, instance, created, **kwargs):
    pass
