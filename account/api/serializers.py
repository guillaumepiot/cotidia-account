from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers

from account.models import User
from .validators import is_alpha

class SignUpSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100, min_length=2, error_messages={
        'blank': _("Please enter your full name."), 
        'invalid': _("The full name is not valid.")
        })
    email = serializers.EmailField(error_messages={
        'blank': _("Please enter your email."), 
        'unique': _("This email is already used."), 
        'invalid': _("This email address is not valid.")
        })
    password = serializers.CharField(error_messages={
        'blank': _("Please enter a password."), 
        'invalid': _("This password is not valid.")
        })

    def validate_email(self, value):
        email = value.lower().strip()

        if User.objects.filter(email=email.strip()).count() > 0:
            raise serializers.ValidationError(_("This email is already used."))
        return email

    def validate_full_name(self, value):
        full_name = value

        if len(full_name.strip()) > 50:
            raise serializers.ValidationError(_("The full name must be 50 characters long maximum."))
        elif len(full_name.strip()) < 3:
            raise serializers.ValidationError(_("The full name must be at least 3 characters long."))
        elif not is_alpha(full_name.strip()):
            raise serializers.ValidationError(_("The full name field only accepts letters and hyphen."))
        return full_name

    def validate_password(self, value):

        password = value

        if len(password.strip()) < 6:
            raise serializers.ValidationError(_("Password must be at least 6 characters long."))
        elif len(password.strip()) > 50:
            raise serializers.ValidationError(_("Password must be 50 characters long maximum."))
        return password


class SignInTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={
        'blank': _("Please enter your email."), 
        'unique': _("This email is already used."), 
        'invalid': _("This email address is not valid.")
        })
    password = serializers.CharField(error_messages={
        'blank': _("Please enter a password."), 
        'invalid': _("This password is not valid.")
        })
    remember_me = serializers.CharField(required=False)

    def validate_email(self, value):
        email = value.lower().strip()
        return email

    def validate_password(self, value):

        password = value

        if len(password.strip()) < 6:
            raise serializers.ValidationError(_("Password must be at least 6 characters long."))
        elif len(password.strip()) > 50:
            raise serializers.ValidationError(_("Password must be 50 characters long maximum."))
        return password

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError(_('Your user account is not active.'))
                self.user = user
                return attrs
            else:
                raise serializers.ValidationError(_('The email and password combination is invalid.'))
        else:
            raise serializers.ValidationError(_('Please include an email and a password.'))

class AuthenticateTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['email', 'first_name', 'last_name']