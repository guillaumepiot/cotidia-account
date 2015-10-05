from django.http import HttpResponse, HttpRequest, HttpResponseRedirect  
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext              
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.views import login
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages


from account.forms import UpdateDetailsForm

@login_required
def dashboard(request):
    template = 'admin/account/dashboard.html'
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
            return HttpResponseRedirect(reverse('my_account'))
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