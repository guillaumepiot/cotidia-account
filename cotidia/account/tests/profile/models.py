from django.db import models


class Profile(models.Model):
    user = models.OneToOneField('account.User')
    company = models.CharField(max_length=50, null=True)
