from django import forms
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField,
    AdminPasswordChangeForm
)
from django.urls import reverse

from betterforms.forms import BetterModelForm, BetterForm

from cotidia.account.models import User


class UserAddForm(BetterModelForm):

    email = forms.EmailField(required=True)

    groups = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Group.objects.all(),
        required=False)

    user_permissions = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Permission.objects.all(),
        required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        ]
        fieldsets = (
            ('info', {'fields': (('first_name', 'last_name'), ('email', 'username'),), 'legend': 'User details'}),
            # ('security', {'fields': ('password',), 'legend': 'Security'}),
            ('role', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), 'legend': 'Roles & Permissions'}),
        )


class UserUpdateForm(UserAddForm, UserChangeForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "password"
        ]
        fieldsets = (
            ('info', {'fields': (('first_name', 'last_name'), ('email', 'username'),), 'legend': 'User details'}),
            ('security', {'fields': ('password',), 'legend': 'Security'}),
            ('role', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), 'legend': 'Roles & Permissions'}),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs["instance"]

        self.fields['password'].help_text = _(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password. <br><a href=\"{}\" class=\"btn btn--small\">Change password</a>".format(
                reverse("account-admin:user-change-password", args=[instance.id]))
        )


class UserInviteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []


class UserChangePasswordForm(BetterForm, AdminPasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

    class Meta:
        # model = User
        # fields = [
        #     "password1",
        #     "password2",
        #     "email",
        #     "username",
        #     "is_active",
        #     "is_staff",
        #     "is_superuser",
        #     "groups",
        #     "user_permissions",
        #     "password"
        # ]
        fieldsets = (
            ('info', {'fields': ('password1', 'password2'), 'legend': 'Change password'}),
        )
