from django import forms

from two_factor.forms import (
    AuthenticationTokenForm as BaseAuthenticationTokenForm,
    BackupTokenForm as BaseBackupTokenForm,
    TOTPDeviceForm as BaseTOTPDeviceForm,
    PhoneNumberForm as BasePhoneNumberForm,
    DeviceValidationForm as BaseDeviceValidationForm,
    PhoneNumberMethodForm as BasePhoneNumberMethodForm,
    MethodForm as BaseMethodForm
)
from two_factor.utils import totp_digits
from two_factor.validators import validate_international_phonenumber


class AuthenticationTokenForm(BaseAuthenticationTokenForm):
    otp_token = forms.IntegerField(
        label="Token",
        min_value=1,
        max_value=int('9' * totp_digits()),
        widget=forms.TextInput(
            attrs={'placeholder': "Token", 'class': 'form__text'}
            ),
        required=False
        )


class BackupTokenForm(BaseBackupTokenForm):
    otp_token = forms.CharField(
        label="Token",
        widget=forms.TextInput(
            attrs={'placeholder': "Backup Token", 'class': 'form__text'}
            ),
        required=False
        )


class PasswordProtectionForm(forms.Form):
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'placeholder': "Password", 'class': 'form__text'}
            )
        )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        if not self.user.check_password(password):
            raise forms.ValidationError('Invalid password')


class EmptyForm(forms.Form):
    pass


class MethodForm(BaseMethodForm):
    method = forms.ChoiceField(
        label="Method",
        initial='generator',
        widget=forms.RadioSelect())


class TOTPDeviceForm(BaseTOTPDeviceForm):
    token = forms.IntegerField(
        label="Token",
        min_value=0,
        max_value=int('9' * totp_digits()),
        widget=forms.TextInput(
            attrs={'placeholder': "Token", 'class': 'form__text'}
            ),
        required=False
        )


class PhoneNumberForm(BasePhoneNumberForm):
    number = forms.CharField(
        label="Phone Number",
        validators=[validate_international_phonenumber],
        widget=forms.TextInput(
            attrs={'placeholder': "+1 123 333 4444", 'class': 'form__text'}
            ),
        required=False,
        help_text="Must start with country code. Eg: +1, +44"
        )


class DeviceValidationForm(BaseDeviceValidationForm):
    token = forms.IntegerField(
        label="Token",
        min_value=1,
        max_value=int('9' * totp_digits()),
        widget=forms.TextInput(
            attrs={'placeholder': "Token", 'class': 'form__text'}
            ),
        required=False
        )


class YubiKeyDeviceForm(DeviceValidationForm):
    token = forms.CharField(
        label="YubiKey",
        widget=forms.TextInput(
            attrs={'placeholder': "Token", 'class': 'form__text'}
            )
        )


class PhoneNumberMethodForm(BasePhoneNumberMethodForm):
    number = forms.CharField(
        label="Phone Number",
        validators=[validate_international_phonenumber],
        widget=forms.TextInput(
            attrs={'placeholder': "+1 123 333 4444", 'class': 'form__text'}
            ),
        help_text="Must start with country code. Eg: +1, +44"
        )
    method = forms.ChoiceField(
        label="Method",
        initial='generator',
        widget=forms.RadioSelect())
