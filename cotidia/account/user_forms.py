from django import forms
from django.contrib.auth.forms import (
    AdminPasswordChangeForm
)

from cotidia.account.models import User


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
