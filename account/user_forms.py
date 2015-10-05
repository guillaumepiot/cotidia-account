from django import forms
from django.utils.translation import ugettext_lazy as _
from form_utils.forms import BetterModelForm

from account.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import ( 
    UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, AdminPasswordChangeForm
    )

class UserForm(forms.Form):

    username = forms.CharField(
        label='', 
        max_length=256, 
        widget=forms.TextInput(attrs={'placeholder':_("Username"), 'class':'form__text'})
        )

    first_name = forms.CharField(
        label='', 
        max_length=256, 
        widget=forms.TextInput(attrs={'placeholder':_("First name"), 'class':'form__text'})
        )

    last_name = forms.CharField(
        label='', 
        max_length=256, 
        widget=forms.TextInput(attrs={'placeholder':_("Last name"), 'class':'form__text'})
        )

    email = forms.EmailField(
        label='', 
        max_length=256, 
        widget=forms.TextInput(attrs={'placeholder':_("Email"), 'class':'form__text'})
        )

    groups = forms.ModelMultipleChoiceField(
        label='',
        widget=forms.CheckboxSelectMultiple,
        queryset=Group.objects.all(),
        required=False)

    user_permissions = forms.ModelMultipleChoiceField(
        label='',
        widget=forms.CheckboxSelectMultiple,
        queryset=Permission.objects.all(),
        required=False)

class UserAddForm(UserForm, UserCreationForm):

    password1 = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'placeholder':_("Password"), 'class':'form__text'}))

    password2 = forms.CharField(label='',
        widget=forms.PasswordInput(attrs={'placeholder':_("Password Confirmation"), 'class':'form__text'}),
        help_text=_("Enter the same password as before, for verification."))

    class Meta:
        model = User
        exclude = ('password', 'date_joined', 'last_login')


class UserUpdateForm(UserForm, UserChangeForm):

    password = ReadOnlyPasswordHashField(label='',
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password."))

    class Meta:
        model = User
        exclude = ('date_joined', 'last_login')

class GroupForm(forms.ModelForm):

    name = forms.CharField(
        label='', 
        max_length=256, 
        widget=forms.TextInput(attrs={'class':'form__text'})
        )

    permissions = forms.ModelMultipleChoiceField(
        label='',
        widget=forms.CheckboxSelectMultiple,
        queryset=Permission.objects.all(),
        required=False)

    class Meta:
        model = Group
        fields = ['name', 'permissions']

class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        label='', 
        max_length=256, 
        widget=forms.TextInput(attrs={'placeholder':_("Username"), 'class':'form__text'})
        )

    first_name = forms.CharField(
        label='', 
        max_length=256, 
        widget=forms.TextInput(attrs={'placeholder':_("First name"), 'class':'form__text'})
        )

    last_name = forms.CharField(
        label='', 
        max_length=256, 
        widget=forms.TextInput(attrs={'placeholder':_("Last name"), 'class':'form__text'})
        )

    email = forms.EmailField(
        label='', 
        max_length=256, 
        widget=forms.TextInput(attrs={'placeholder':_("Email"), 'class':'form__text'})
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

class UserChangePassword(AdminPasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserChangePassword, self).__init__(*args, **kwargs)

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder':"", 'class':'form__text'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder':_("Confirm Password"), 'class':'form__text'})
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""
        self.fields['password2'].help_text=_("Enter the same password again, for verification.")
