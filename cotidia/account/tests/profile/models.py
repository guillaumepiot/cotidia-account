from django.db import models


class Profile(models.Model):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE)
    company = models.CharField(max_length=50, null=True)
