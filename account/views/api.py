import hashlib

from django.conf import settings
from django.utils.timezone import now
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from account.serializers import (
    SignUpSerializer,
    SignInTokenSerializer,
    AuthenticateTokenSerializer,
    UserSerializer,
    ResetPasswordSerializer,
    SetPasswordSerializer
    )
from account.models import User
from account.notices import (
    NewUserActivationNotice,
    ResetPasswordNotice
    )
from account import settings as account_settings


class SignUp(APIView):
    """Handle the creation of a new account."""

    authentication_classes = ()
    permission_classes = ()
    serializer_class = SignUpSerializer

    def get_serializer_class(self):
        return self.serializer_class

    @transaction.atomic
    def post(self, request):

        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():

            full_name = serializer.data['full_name'].strip()
            if len(full_name.split(' ')) > 1:
                first_name = full_name.split(' ')[0]
                last_name = ' '.join(full_name.split(' ')[1:])
            else:
                first_name = full_name
                last_name = ''

            email = serializer.data['email'].strip()
            password = serializer.data['password'].strip()

            m = hashlib.md5()
            m.update(email.encode('utf-8'))
            username = m.hexdigest()[0:30]

            if account_settings.ACCOUNT_FORCE_ACTIVATION is True:
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

            if account_settings.ACCOUNT_FORCE_ACTIVATION is True:

                # Create and send the confirmation email
                token = default_token_generator.make_token(user)

                if hasattr(settings, 'APP_URL'):
                    APP_URL = settings.APP_URL
                else:
                    APP_URL = settings.SITE_URL

                url = '{0}/activate/{1}/{2}/'.format(APP_URL, user.uuid, token)

                notice = NewUserActivationNotice(
                    recipients=['{0} <{1}>'.format(
                        user.get_full_name(), user.email
                        )],
                    context={
                        'url': url,
                        'first_name': user.first_name
                    }
                )
                notice.send(force_now=True)

            token, created = Token.objects.get_or_create(user=user)

            data = {'token': token.key}
            user = UserSerializer(token.user)
            data.update(user.data)

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignIn(APIView):
    """Sign in a user with email and password."""

    authentication_classes = ()
    permission_classes = ()
    serializer_class = SignInTokenSerializer
    model = Token

    def get_serializer_class(self):
        return self.serializer_class

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            user = authenticate(
                username=serializer.data['email'],
                password=serializer.data['password']
                )
            auth_login(request, user)

            token, created = Token.objects.get_or_create(user=user)

            data = {'token': token.key}
            user = UserSerializer(token.user)
            data.update(user.data)

            return Response(data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activate(APIView):
    """Activate a profile."""

    authentication_classes = ()
    permission_classes = ()

    @transaction.atomic
    def get(self, request, uuid, token):

        try:
            user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return Response(
                {'message': 'USER_INVALID'},
                status=status.HTTP_400_BAD_REQUEST
                )

        if not default_token_generator.check_token(user, token):
            return Response(
                {'message': 'TOKEN_INVALID'},
                status=status.HTTP_400_BAD_REQUEST
                )

        # Activate now
        user.is_active = True
        user.save()

        return Response({'message': 'ACTIVATED'}, status=status.HTTP_200_OK)


class Authenticate(APIView):
    """Authenticate with a given token."""

    authentication_classes = ()
    permission_classes = ()
    serializer_class = AuthenticateTokenSerializer

    def get_serializer_class(self):
        return self.serializer_class

    @transaction.atomic
    def post(self, request, user_serializer_class=None):

        if user_serializer_class is None:
            user_serializer_class = UserSerializer

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                token = Token.objects.get(key=serializer.data['token'])
            except Token.DoesNotExist:
                return Response(
                    {'message': 'TOKEN_INVALID'},
                    status=status.HTTP_400_BAD_REQUEST)

            if not token.user.is_active:
                return Response(
                    {'message': 'USER_INACTIVE'},
                    status=status.HTTP_400_BAD_REQUEST)

            user = user_serializer_class(token.user)

            return Response(user.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """Reset the password for an exiting user."""

    authentication_classes = ()
    permission_classes = ()

    @transaction.atomic
    def post(self, request):

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.data['email'])
        except User.DoesNotExist:
            user = None

        if user:

            token = default_token_generator.make_token(user)

            if hasattr(settings, 'APP_URL'):
                APP_URL = settings.APP_URL
            else:
                APP_URL = settings.SITE_URL

            url = '{0}/reset-password/{1}/{2}/'.format(
                APP_URL, user.uuid, token)

            notice = ResetPasswordNotice(
                recipients=['%s <%s>' % (user.get_full_name(), user.email)],
                context={
                    'url': url,
                    'first_name': user.first_name
                }
            )
            notice.send(force_now=True)

        return Response(
            {'message': "PASSWORD_RESET"},
            status=status.HTTP_200_OK
            )


class ResetPasswordValidate(APIView):
    """Validate the reset password key."""

    authentication_classes = ()
    permission_classes = ()

    @transaction.atomic
    def get(self, request, uuid, token):

        try:
            user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return Response(
                {'message': "USER_INVALID"},
                status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response(
                {'message': "TOKEN_INVALID"},
                status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': "TOKEN_VALID"}, status=status.HTTP_200_OK)


class SetPassword(APIView):
    """Set the new password."""

    authentication_classes = ()
    permission_classes = ()

    @transaction.atomic
    def post(self, request, uuid, token):

        try:
            user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return Response(
                {'message': "USER_INVALID"},
                status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response(
                {'message': "TOKEN_INVALID"},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #
        # Set the new password
        #
        user.set_password(serializer.data['password1'])
        user.save()

        return Response({'message': "PASSWORD_SET"}, status=status.HTTP_200_OK)


class UpdateDetails(APIView):
    """Update the user details."""

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    @transaction.atomic
    def post(self, request):

        serializer = UserSerializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
