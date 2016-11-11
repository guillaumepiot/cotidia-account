from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(
            self,
            email=None,
            password=None,
            first_name="",
            last_name="",
            **kwargs):
        """Create and save a user."""

        user = self.model(
            first_name=first_name.title(),
            last_name=last_name.title(),
            email=self.normalize_email(email),
            username=self.create_username(first_name, last_name)
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, first_name, last_name):
        """Create and save a superuser."""

        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_username(self, first_name, last_name):
        """Generate a username from the first and last name."""
        return (first_name+last_name).lower().replace(' ', '')
