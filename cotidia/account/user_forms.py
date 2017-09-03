from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    ReadOnlyPasswordHashField,
    AdminPasswordChangeForm
)

from cotidia.account.models import User


class UserForm(forms.ModelForm):

    username = forms.CharField(max_length=256)
    first_name = forms.CharField(max_length=256)
    last_name = forms.CharField(max_length=256)

    email = forms.EmailField()

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
        exclude = []


class UserAddForm(UserForm, UserCreationForm):

    username = forms.CharField(
        max_length=256,
        help_text=(
            "Usernames must be unique. You can use the email address."
        )
    )

    class Meta:
        model = User
        exclude = ('password', 'date_joined', 'last_login')


class UserUpdateForm(UserForm, UserChangeForm):

    password = ReadOnlyPasswordHashField(
        label='',
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password."))

    class Meta:
        model = User
        exclude = ('date_joined', 'last_login')


class ProfileForm(forms.ModelForm):

    username = forms.CharField(max_length=256)
    first_name = forms.CharField(max_length=256)
    last_name = forms.CharField(max_length=256)
    email = forms.EmailField(max_length=256)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UserChangePassword(AdminPasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserChangePassword, self).__init__(*args, **kwargs)

        # self.fields['password1'].widget = forms.PasswordInput(
        #     attrs={'placeholder': "", 'class': 'form__text'})
        # self.fields['password2'].widget = forms.PasswordInput(
        #     attrs={
        #         'placeholder': _("Confirm Password"),
        #         'class': 'form__text'
        #         }
        #     )
        # self.fields['password1'].label = ""
        # self.fields['password2'].label = ""
        # self.fields['password2'].help_text = _(
        #     "Enter the same password again, for verification."
        #     )
