from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, resolve_url
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.http import is_safe_url

from cotidia.account.conf import settings
from cotidia.account.user_forms import (
    ProfileForm
)


@sensitive_post_parameters()
@csrf_protect
def login_remember_me(
        request,
        authentication_form=None,
        template_name='admin/account/login.html',
        *args,
        **kwargs):
    """Custom login view that enables "remember me" functionality."""

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('account-admin:dashboard'))

    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

    if request.GET.get('next'):
        redirect_to = request.GET['next']
    else:
        redirect_to = reverse('account-admin:dashboard')

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    context = {
        'form': form
    }

    return render(request, template_name, context)


@login_required(login_url=settings.ACCOUNT_ADMIN_LOGIN_URL)
def dashboard(request):

    if not request.user.is_staff:
        raise PermissionDenied

    template = 'admin/account/dashboard.html'
    return render(request, template)


@login_required(login_url=settings.ACCOUNT_ADMIN_LOGIN_URL)
def edit(request, user_form=ProfileForm):

    if not request.user.is_staff:
        raise PermissionDenied

    template = 'admin/account/edit.html'

    if request.method == "POST":
        form = user_form(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                _('Your personal details have been saved')
            )
            return HttpResponseRedirect(
                reverse('account-admin:dashboard')
            )
    else:
        form = user_form(instance=request.user)

    return render(request, template, {'form': form})


