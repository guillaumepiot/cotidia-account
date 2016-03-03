import datetime, time, hashlib

from django.utils.text import slugify
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login

from rest_framework import status, generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from account.api.serializers import (
    SignUpSerializer, 
    SignInTokenSerializer, 
    AuthenticateTokenSerializer, 
    UserSerializer
    )
from account.models import User
from account.utils import send_activation_email


class SignUp(APIView):
    """
    Handle the creation of a new account
    """

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

            # Create the user
            user = User.objects.create(
                username=username,
                email=email, 
                first_name=first_name,
                last_name=last_name,
                last_login=now()
                )
            user.set_password(password)
            user.save()


            # Create and send the confirmation email
            send_activation_email(user)

            token, created = Token.objects.get_or_create(user=user)
            
            data = {'token': token.key}
            user = UserSerializer(token.user)
            data.update(user.data)

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignIn(APIView):
    """
    Sign in a user with email and password
    """

    authentication_classes = ()
    permission_classes = ()
    serializer_class = SignInTokenSerializer

    def get_serializer_class(self):
        return self.serializer_class

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            if not serializer.data.get('remember_me'):
                self.request.session.set_expiry(0)

            user = authenticate(username=serializer.data['email'], password=serializer.data['password'])
            auth_login(request, user)

            # Create token for native applications

            token, created = Token.objects.get_or_create(user=user)

            data = {'token': token.key}
            user = UserSerializer(token.user)
            data.update(user.data)
            
            return Response(data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Authenticate(APIView):
    """
    Authenticate with a given token
    """

    authentication_classes = ()
    permission_classes = ()
    serializer_class = AuthenticateTokenSerializer

    def get_serializer_class(self):
        return self.serializer_class

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            try:
                token = Token.objects.get(key=serializer.data['token'])
            except Token.DoesNotExist:
                return Response({'message':_('The token is not valid')}, status=status.HTTP_400_BAD_REQUEST)

            user = UserSerializer(token.user)

            return Response(user.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
