"""
Custom authentication backends.

Inspired by http://djangosnippets.org/snippets/2463/

"""
from django.contrib.auth.backends import ModelBackend
from cotidia.account.conf import settings
from django.core.validators import validate_email
from django.apps import apps


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows to login with an email address.

    """

    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, request=None, username=None, password=None):
        app_label, model_name = settings.AUTH_USER_MODEL.split(".")
        User = apps.get_model(app_label, model_name)

        try:
            validate_email(username)
        except:
            username_is_email = False
        else:
            username_is_email = True

        if username_is_email:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        app_label, model_name = settings.AUTH_USER_MODEL.split(".")
        User = apps.get_model(app_label, model_name)
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
