import hashlib

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.conf import settings

from cotidia.account.forms import UpdateDetailsForm, AccountUserCreationForm
from cotidia.account.models import User
from cotidia.account import settings as account_settings
from cotidia.account.notices import (
    NewUserActivationNotice
    )


@login_required
def dashboard(request):
    """Dashboard view for public users."""

    template = 'account/dashboard.html'
    return render(request, template, {})


@login_required
def edit(request):
    """Edit details view for logged in public user."""

    template = 'account/edit.html'

    if request.method == "POST":
        form = UpdateDetailsForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _('Your personal details have been saved'))
            return HttpResponseRedirect(reverse('account-public:dashboard'))
    else:
        form = UpdateDetailsForm(instance=request.user)

    return render(request, template, {'form': form})


def login_remember_me(request, *args, **kwargs):
    """Custom login view that enables "remember me" functionality."""

    if account_settings.ACCOUNT_ALLOW_SIGN_IN is False:
        raise Http404

    # Redirect to account page if already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account-public:dashboard'))
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

    extra_context = {}
    if request.GET.get('next'):
        extra_context['success_url'] = request.GET['next']

    return login(request, extra_context=extra_context, *args, **kwargs)


def sign_up(request):
    """Sign up view for public user."""

    if account_settings.ACCOUNT_ALLOW_SIGN_UP is False:
        raise Http404

    template = 'account/sign_up.html'
    form = AccountUserCreationForm()

    success_url = request.GET.get('next')

    # Redirect to account page if already logged in
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account-public:dashboard'))

    if request.method == "POST":
        form = AccountUserCreationForm(request.POST)
        if form.is_valid():
            user = User(email=form.cleaned_data["email"])
            user.set_password(form.cleaned_data["password1"])
            # Hash the email address to generate a unique username
            m = hashlib.md5()
            m.update(form.cleaned_data["email"].encode('utf-8'))
            user.username = m.hexdigest()[0:30]
            user.save()

            if account_settings.ACCOUNT_FORCE_ACTIVATION is True:
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
            token = default_token_generator.make_token(user)
            url = reverse('account-public:activate', kwargs={
                'uuid': user.uuid,
                'token': token
                })

            notice = NewUserActivationNotice(
                recipients=['%s <%s>' % (user.get_full_name(), user.email)],
                context={
                    'url': "{0}{1}".format(settings.SITE_URL, url),
                    'first_name': user.first_name
                }
            )
            notice.send(force_now=True)

            if account_settings.ACCOUNT_FORCE_ACTIVATION is True:
                return HttpResponseRedirect(
                    reverse('account-public:activation-pending'))
            elif success_url:
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(
                    reverse('account-public:dashboard'))

    context = {'form': form, 'success_url': success_url}
    return render(request, template, context)


def activate(request, uuid, token, template_name):
    """Activate view for a public user who just signed up."""

    user = get_object_or_404(User, uuid=uuid)

    # Use PASSWORD_RESET_TIMEOUT_DAYS to set the confirmation date limit
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

    return render(request, template_name, {'user': user})


def activation_pending(request, template_name):
    """Activation pending view for a public user."""
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account-public:dashboard'))

    return render(request, template_name, {})