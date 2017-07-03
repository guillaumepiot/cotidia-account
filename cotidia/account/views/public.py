import hashlib

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from cotidia.account.conf import settings

from cotidia.account.forms import (
    UpdateDetailsForm,
    AccountUserCreationForm,
    EmailAuthenticationForm
    )
from cotidia.account.models import User
from cotidia.account import signals


@login_required
def dashboard(request):
    """Dashboard view for public users."""

    template = 'account/dashboard.html'
    return render(request, template, {})


@login_required
def edit(
        request,
        edit_form=UpdateDetailsForm,
        template_name='account/edit.html'
        ):
    """Edit details view for logged in public user."""

    if request.method == "POST":
        form = edit_form(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _('Your personal details have been saved'))
            return HttpResponseRedirect(reverse('account-public:dashboard'))
    else:
        form = edit_form(instance=request.user)

    return render(request, template_name, {'form': form})


class LoginView(AuthLoginView):
    template_name = 'account/login.html'
    form_class = EmailAuthenticationForm

    def get(self, *args, **kwargs):
        if settings.ACCOUNT_ALLOW_SIGN_IN is False:
            raise Http404
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(self.redirect_url)
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.POST.get('remember_me', None) is not None:
            self.request.session.set_expiry(0)
        return super().post(*args, **kwargs)


def sign_up(
        request,
        sign_up_form=AccountUserCreationForm,
        template_name='account/sign_up.html'):
    """Sign up view for public user."""

    if settings.ACCOUNT_ALLOW_SIGN_UP is False:
        raise Http404

    form = sign_up_form()

    success_url = request.GET.get('next')

    # Redirect to account page if already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account-public:dashboard'))

    if request.method == "POST":
        form = sign_up_form(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data["password1"])
            # Hash the email address to generate a unique username
            m = hashlib.md5()
            m.update(form.cleaned_data["email"].encode('utf-8'))
            user.username = m.hexdigest()[0:30]
            user.save()

            if settings.ACCOUNT_FORCE_ACTIVATION is True:
                user.is_active = False
                user.save()
            else:
                # Log the user straight away
                new_user = authenticate(
                    username=user.username,
                    password=form.cleaned_data['password1']
                    )
                auth_login(request, new_user)
                messages.success(
                    request, _('Your have successfully signed up'))

            # Create and send the confirmation email
            user.send_activation_link(app=False)

            # Send the activation signals
            signals.user_sign_up.send(
                sender=None,
                request=request,
                user=user)

            if settings.ACCOUNT_FORCE_ACTIVATION is True:
                return HttpResponseRedirect(
                    reverse(
                        'account-public:activation-pending',
                        kwargs={
                            'uuid': user.uuid
                            })
                        )
            elif success_url:
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(
                    reverse('account-public:dashboard'))

    context = {'form': form, 'success_url': success_url}
    return render(request, template_name, context)


def activate(request, uuid, token, template_name):
    """Activate view for a public user who just signed up."""

    user = get_object_or_404(User, uuid=uuid)

    # Use PASSWORD_RESET_TIMEOUT_DAYS to set the confirmation date limit
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

    # Authenticate the user straight away
    auth_login(request, user)

    # Send the activation signals
    signals.user_activate.send(
        sender=None,
        request=request,
        user=user)

    return render(request, template_name, {'user': user})


def activation_pending(request, uuid, template_name):
    """Activation pending view for a public user."""

    user = get_object_or_404(User, uuid=uuid)

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account-public:dashboard'))

    return render(request, template_name, {"user": user})


def resend_activation_link(request, uuid):
    """Resend the activation link for a user."""

    user = get_object_or_404(User, uuid=uuid)
    user.send_activation_link(app=False)

    messages.success(
        request, "The activate link has been resent to your email address.")

    return HttpResponseRedirect(
            reverse(
                "account-public:activation-pending",
                kwargs={"uuid": user.uuid}
            )
        )
