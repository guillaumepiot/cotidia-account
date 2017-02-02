import hashlib

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.utils.timezone import now
from cotidia.account.conf import settings

from rest_framework import serializers

from cotidia.account.models import User
from cotidia.account.validators import is_alpha


class SignUpSerializer(serializers.Serializer):
    full_name = serializers.CharField(
        max_length=100,
        min_length=2,
        error_messages={
            'required': _("Please enter your full name."),
            'blank': _("Please enter your full name."),
            'invalid': _("The full name is not valid.")
        })
    email = serializers.EmailField(
        error_messages={
            'required': _("Please enter your email."),
            'blank': _("Please enter your email."),
            'unique': _("This email is already used."),
            'invalid': _("This email address is not valid.")
        })
    password = serializers.CharField(
        error_messages={
            'required': _("Please enter a password"),
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
            raise serializers.ValidationError(
                _("The full name must be 50 characters long maximum.")
                )
        elif len(full_name.strip()) < 3:
            raise serializers.ValidationError(
                _("The full name must be at least 3 characters long.")
                )
        elif not is_alpha(full_name.strip()):
            raise serializers.ValidationError(
                _(
                    "The full name field only accepts letters, hyphen "
                    "and apostrophe."
                )
                )
        return full_name

    def validate_password(self, value):

        password = value

        if len(password.strip()) < 6:
            raise serializers.ValidationError(
                _("Password must be at least 6 characters long.")
                )
        elif len(password.strip()) > 50:
            raise serializers.ValidationError(
                _("Password must be 50 characters long maximum.")
                )
        return password

    def create(self, validated_data):

        full_name = validated_data["full_name"].strip()
        if len(full_name.split(' ')) > 1:
            first_name = full_name.split(' ')[0]
            last_name = ' '.join(full_name.split(' ')[1:])
        else:
            first_name = full_name
            last_name = ''

        email = validated_data["email"].strip()
        password = validated_data["password"].strip()

        m = hashlib.md5()
        m.update(email.encode("utf-8"))
        username = m.hexdigest()[0:30]

        if settings.ACCOUNT_FORCE_ACTIVATION is True:
            active = False
        else:
            active = True

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            last_login=now(),
            is_active=active
            )
        user.set_password(password)
        user.save()

        return user


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
            raise serializers.ValidationError(
                _("Password must be at least 6 characters long.")
                )
        elif len(password.strip()) > 50:
            raise serializers.ValidationError(
                _("Password must be 50 characters long maximum.")
                )
        return password

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        _("Your account is not active.")
                        )
                self.user = user
                return attrs
            else:
                raise serializers.ValidationError(
                    _("The email and password combination is invalid.")
                    )
        else:
            raise serializers.ValidationError(
                _("Please include an email and a password.")
                )


class AuthenticateTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        error_messages={
            'required': "Please enter your first name.",
            'blank': "The first name may not be blank.",
            'invalid': "The first name is not valid."
        }
    )
    last_name = serializers.CharField(
        error_messages={
            'required': "Please enter your last name.",
            'blank': "The last name may not be blank.",
            'invalid': "The last name is not valid."
        }
    )
    email = serializers.EmailField(
        error_messages={
            'required': "Please enter your email.",
            'blank': "The email may not be blank.",
            'invalid': "The email is not valid."
        }
    )

    class Meta:
        model = User
        fields = [
            'uuid',
            'email',
            'first_name',
            'last_name'
            ]


#
# Requires the user to submit his email to receive a reset password link
#
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={
        'required': _("Please enter your email."),
        'invalid': _("This email address is not valid.")
        })

    def validate_email(self, value):
        """Force the email to be lowercase with trailing white spaces."""
        email = value.lower().strip()
        return email


#
# Allow the creation of a new password when the user resetted it
#
class SetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(error_messages={
        'required': "PASSWORD_REQUIRED",
        'invalid': "PASSWORD_INVALID"
        })
    password2 = serializers.CharField(error_messages={
        'required': "PASSWORD_REQUIRED",
        'invalid': "PASSWORD_INVALID"
        })

    def validate_password1(self, value):

        password = value

        if len(password.strip()) < 6:
            raise serializers.ValidationError("PASSWORD_TOO_SHORT")
        elif len(password.strip()) > 50:
            raise serializers.ValidationError("PASSWORD_TOO_LONG")
        return password

    def validate(self, data):

        if data['password1'] != data['password2']:
            raise serializers.ValidationError("PASSWORD_MISMATCH")

        return data
