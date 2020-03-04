from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views import View
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.contrib import messages

from django_otp import devices_for_user, user_has_device
from django_otp.decorators import otp_required
from django_otp.plugins.otp_static.models import StaticToken

from two_factor.models import get_available_phone_methods
from two_factor.views.utils import class_view_decorator
from two_factor.views.core import (
    LoginView as BaseLoginView,
    BackupTokensView as BaseBackupTokensView,
    SetupView as BaseSetupView,
    SetupCompleteView as BaseSetupCompleteView,
    PhoneSetupView as BasePhoneSetupView,
    PhoneDeleteView as BasePhoneDeleteView,
)
from two_factor.views.profile import ProfileView as BaseProfileView

from cotidia.account.forms import (
    EmailAuthenticationForm,
    AuthenticationTokenForm,
    BackupTokenForm,
    PasswordProtectionForm,
    EmptyForm,
    MethodForm,
    TOTPDeviceForm,
    PhoneNumberForm,
    DeviceValidationForm,
    YubiKeyDeviceForm,
    PhoneNumberMethodForm,
)
from cotidia.account.models import User


@class_view_decorator(sensitive_post_parameters())
@class_view_decorator(never_cache)
class TwoFactorLoginView(BaseLoginView):
    template_name = "admin/account/two_factor/core/login.html"
    form_list = (
        ("auth", EmailAuthenticationForm),
        ("token", AuthenticationTokenForm),
        ("backup", BackupTokenForm),
    )

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["next"] = self.request.GET.get("next") or reverse(
            "account-admin:dashboard"
        )
        return context


@class_view_decorator(never_cache)
@class_view_decorator(otp_required)
class BackupTokensView(BaseBackupTokensView):
    redirect_url = "account-admin:backup_tokens"
    template_name = "admin/account/two_factor/core/backup_tokens.html"


@class_view_decorator(never_cache)
@class_view_decorator(login_required)
class ProfileView(BaseProfileView):
    template_name = "admin/account/two_factor/profile/profile.html"


@class_view_decorator(never_cache)
@class_view_decorator(otp_required)
class DisableView(View):
    """View for disabling two-factor for a user's account."""

    template_name = "admin/account/two_factor/profile/disable.html"
    redirect_url = None
    form_class = PasswordProtectionForm

    def get(self, request, *args, **kwargs):

        if not user_has_device(self.request.user):
            return redirect(resolve_url("account-admin:edit"))

        form = self.form_class(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, user=request.user)

        if form.is_valid():
            # Remove all the devices from the user
            for device in devices_for_user(self.request.user):
                device.delete()

            return redirect(resolve_url("account-admin:edit"))

        return render(request, self.template_name, {"form": form})


@class_view_decorator(never_cache)
@class_view_decorator(otp_required)
class UserDisableView(View):
    """View for disabling two-factor for another user's account.

    This view is restricted to superusers only.
    """

    template_name = "admin/account/two_factor/profile/disable.html"
    redirect_url = None
    form_class = PasswordProtectionForm

    def get_user(self, uuid):
        return get_object_or_404(User, uuid=uuid)

    def get(self, request, uuid, *args, **kwargs):

        # Superuser only.
        if not request.user.is_superuser:
            raise PermissionDenied

        user = self.get_user(uuid)

        if not user_has_device(user):
            return redirect(resolve_url("account-admin:user-detail", pk=user.id))

        form = self.form_class(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, uuid, *args, **kwargs):

        # Superuser only.
        if not request.user.is_superuser:
            raise PermissionDenied

        form = self.form_class(data=request.POST, user=request.user)

        if form.is_valid():

            user = self.get_user(uuid)

            # Remove all the devices from the user
            for device in devices_for_user(user):
                device.delete()

            return redirect(resolve_url("account-admin:user-detail", pk=user.id))

        return render(request, self.template_name, {"form": form})


@class_view_decorator(never_cache)
@class_view_decorator(otp_required)
class ListBackupTokensView(View):
    """View for listing backup tokens with password protection."""

    form_class = PasswordProtectionForm
    template_name = "admin/account/two_factor/core/list_backup_tokens.html"

    def get_device(self):
        return self.request.user.staticdevice_set.get_or_create(name="backup")[0]

    @property
    def has_backup_tokens(self, **kwargs):
        device = self.get_device()
        if device.token_set.count() > 0:
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return render(
            request,
            self.template_name,
            {"form": form, "has_backup_tokens": self.has_backup_tokens},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, user=request.user)
        context = {"form": form, "has_backup_tokens": self.has_backup_tokens}
        if form.is_valid():
            # Add the device to the context to retrieve the list of tokens
            context["device"] = self.get_device()

        return render(request, self.template_name, context)


@class_view_decorator(never_cache)
@class_view_decorator(otp_required)
class GenerateBackupTokensView(View):
    """Generate backup tokens with password protection."""

    form_class = PasswordProtectionForm
    template_name = "admin/account/two_factor/core/generate_backup_tokens.html"
    initial = {}
    number_of_tokens = 10

    def get_device(self):
        return self.request.user.staticdevice_set.get_or_create(name="backup")[0]

    def get_context_data(self, **kwargs):
        context = super(ListBackupTokensView, self).get_context_data(**kwargs)
        context["device"] = self.get_device()
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial, user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, user=request.user)
        context = {"form": form}
        if form.is_valid():
            # Delete the existing tokens and generate some new ones
            device = self.get_device()
            device.token_set.all().delete()
            for n in range(self.number_of_tokens):
                device.token_set.create(token=StaticToken.random_token())

            context["device"] = device

        return render(request, self.template_name, context)


@class_view_decorator(never_cache)
@class_view_decorator(login_required)
class SetupView(BaseSetupView):
    success_url = "account-admin:setup_complete"
    qrcode_url = "account-admin:qr"
    template_name = "admin/account/two_factor/core/setup.html"
    form_list = (
        ("welcome", EmptyForm),
        ("method", MethodForm),
        ("generator", TOTPDeviceForm),
        ("sms", PhoneNumberForm),
        ("call", PhoneNumberForm),
        ("validation", DeviceValidationForm),
        ("yubikey", YubiKeyDeviceForm),
    )


@class_view_decorator(never_cache)
@class_view_decorator(otp_required)
class SetupCompleteView(BaseSetupCompleteView):
    template_name = "admin/account/two_factor/core/setup_complete.html"


@class_view_decorator(never_cache)
@class_view_decorator(otp_required)
class PhoneSetupView(BasePhoneSetupView):
    success_url = "account-admin:profile"
    template_name = "admin/account/two_factor/core/phone_register.html"
    form_list = (("setup", PhoneNumberMethodForm), ("validation", DeviceValidationForm))

    def get(self, request, *args, **kwargs):
        if not get_available_phone_methods():
            messages.warning(self.request, "No phone or SMS method set.")
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


@class_view_decorator(never_cache)
@class_view_decorator(otp_required)
class PhoneDeleteView(BasePhoneDeleteView):
    def get_success_url(self):
        return resolve_url("account-admin:profile")
