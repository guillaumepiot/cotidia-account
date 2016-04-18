import hashlib

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect  
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext              
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.views import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

from account.forms import UpdateDetailsForm, AccountUserCreationForm
from account.models import User
from account.settings import ACCOUNT_FORCE_ACTIVATION
from account.notices import (
    NewUserActivationNotice
    )

@login_required
def dashboard(request):
    template = 'account/dashboard.html'
    return render_to_response(template, {},
        context_instance=RequestContext(request))
    
@login_required
def edit(request):
    template = 'account/edit.html'
    if request.method == "POST":
        form = UpdateDetailsForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your personal details have been saved'))
            return HttpResponseRedirect(reverse('account-public:dashboard'))
    else:
        form = UpdateDetailsForm(instance=request.user)

    return render_to_response(template, {'form':form},
        context_instance=RequestContext(request))

def login_remember_me(request, *args, **kwargs):
    """Custom login view that enables "remember me" functionality."""
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

    extra_context = {}
    if request.GET.get('next'):
        extra_context['success_url'] = request.GET['next']

    return login(request, extra_context=extra_context, *args, **kwargs)

def sign_up(request):
    template = 'account/sign_up.html'
    form = AccountUserCreationForm()

    success_url = request.GET.get('next')

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

            if ACCOUNT_FORCE_ACTIVATION:
                user.is_active = False
                user.save()
            else:
                # Log the user straight away
                new_user = authenticate(username=user.username, password=form.cleaned_data['password1'])
                auth_login(request, new_user)
                messages.success(request, _('Your have successfully signed up'))

            # Create and send the confirmation email
            token = default_token_generator.make_token(user)
            url = '/activate/{0}/{1}/'.format(user.uuid, token)

            notice = NewUserActivationNotice(
                recipients = ['%s <%s>' % (user.get_full_name(), user.email) ],
                context = {
                    'url':"%s%s" % (settings.APP_URL, url),
                    'first_name':user.first_name
                }
            )
            notice.send(force_now=True)
            
            if ACCOUNT_FORCE_ACTIVATION:
                return HttpResponseRedirect(reverse('account-public:activation-pending'))
            elif success_url:
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(reverse('account-public:dashboard'))

    return render_to_response(template, {'form': form, 'success_url':success_url },
        context_instance=RequestContext(request))


############
# Activate #
############

def activate(request, uuid, token, template_name):

    user = get_object_or_404(User, uuid=uuid)

    #
    # Use PASSWORD_RESET_TIMEOUT_DAYS to set the confirmation date limit
    #
    if default_token_generator.check_token(user, token):
        # Activate now
        user.is_active = True
        user.save()

    return render_to_response(template_name, {'user': user},
        context_instance=RequestContext(request))

def activation_pending(request, template_name):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account-public:dashboard'))

    return render_to_response(template_name, {},
        context_instance=RequestContext(request))