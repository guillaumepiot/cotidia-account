"""
Decorator functions for class methods.

Those decorators are used to decorator any class method, preferably the
`setUp` method which runs at the start of every test, injecting the data and
objects using `self`.

Example:

class APITests(APITestCase):

    @fixtures.admin_user
    def setUp(self):
        pass

"""
from rest_framework.authtoken.models import Token

from cotidia.account.models import User


def superuser(f):
    def wrapper(*args):
        self = args[0]

        self.superuser = User.objects.create(
            first_name="Steve",
            last_name="Green",
            username="steve@green.com",
            email="steve@green.com",
            is_superuser=True,
            is_active=True,
            is_staff=True)
        self.superuser_pwd = 'demo5678'
        self.superuser.set_password(self.superuser_pwd)
        self.superuser.save()
        self.superuser_token, created = Token.objects.get_or_create(
            user=self.superuser)

        return f(*args)
    return wrapper


def admin_user(f):
    def wrapper(*args):
        self = args[0]

        self.admin_user = User.objects.create(
            first_name="John",
            last_name="Blue",
            username="john@blue.com",
            email="john@blue.com",
            is_active=True,
            is_staff=True)
        self.admin_user_pwd = "demo5678"
        self.admin_user.set_password(self.admin_user_pwd)
        self.admin_user.save()
        self.admin_user_token, created = Token.objects.get_or_create(
            user=self.admin_user)

        return f(*args)
    return wrapper


def normal_user(f):
    def wrapper(*args):
        self = args[0]

        self.normal_user = User.objects.create(
            first_name="Bob",
            last_name="Green",
            username="bob@green.com",
            email="bob@green.com",
            is_active=True,
            is_staff=False)
        self.normal_user_pwd = "demo1234"
        self.normal_user.set_password(self.normal_user_pwd)
        self.normal_user.save()
        self.normal_user_token, created = Token.objects.get_or_create(
            user=self.normal_user)

        return f(*args)
    return wrapper


def alt_user(f):
    def wrapper(*args):
        self = args[0]

        self.alt_user = User.objects.create(
            first_name="Al",
            last_name="Ternative",
            username="al@example.com",
            email="al@example.com",
            is_active=True,
            is_staff=False,
        )
        self.alt_user_pwd = "altpass"
        self.alt_user.set_password(self.alt_user_pwd)
        self.alt_user.save()
        self.alt_user_token, created = Token.objects.get_or_create(
            user=self.alt_user,
        )

        return f(*args)
    return wrapper
