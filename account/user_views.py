from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.debug import sensitive_post_parameters
from django.template import RequestContext  
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect 
from django.conf import settings

from account.models import User
from account.user_forms import UserAddForm, UserUpdateForm, GroupForm, ProfileForm, UserChangePassword
from account.utils import StaffPermissionRequiredMixin, import_model
from account import settings as account_settings

#########
# Login #
#########

def login_remember_me(request, *args, **kwargs):
    
    """Custom login view that enables "remember me" functionality."""
    
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

    extra_context = {}
    if request.GET.get('next'):
        extra_context['success_url'] = request.GET['next']
    else:
        extra_context['success_url'] = reverse('account-admin:dashboard')

    return login(request, extra_context=extra_context, *args, **kwargs)

#############
# Dashboard #
#############

@login_required(login_url=account_settings.ADMIN_LOGIN_URL)
def dashboard(request):
    
    # Staff only
    if not request.user.is_staff:
        raise PermissionDenied
    
    template = 'admin/account/dashboard.html'
    return render_to_response(template, {},
        context_instance=RequestContext(request))

@login_required(login_url=account_settings.ADMIN_LOGIN_URL)
def edit(request):

     # Staff only
    if not request.user.is_staff:
        raise PermissionDenied

    template = 'admin/account/edit.html'
    if request.method == "POST":
        form = ProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your personal details have been saved'))
            return HttpResponseRedirect(reverse('account-admin:dashboard'))
    else:
        form = ProfileForm(instance=request.user)

    return render_to_response(template, {'form':form},
        context_instance=RequestContext(request))

########
# User #
########

class UserList(StaffPermissionRequiredMixin, ListView):
    model = User
    template_name = 'admin/account/user_list.html'
    permission_required = 'account.change_user'

    def get_queryset(self):
        return User.objects.filter()

class UserDetail(StaffPermissionRequiredMixin, DetailView):
    model = User
    template_name = 'admin/account/user_detail.html'
    slug_field = 'uuid'
    permission_required = 'account.change_user'

class UserCreate(StaffPermissionRequiredMixin, CreateView):
    model = User
    form_class = UserAddForm
    template_name = 'admin/account/user_form.html'
    permission_required = 'account.add_user'

    def get_success_url(self):
        messages.success(self.request, _('User has been created.'))
        return reverse('account-admin:user_list')

    def get_form_class(self):
        if hasattr(settings, 'ACCOUNT_USER_ADD_FORM'):
            form_class = import_model(settings.ACCOUNT_USER_ADD_FORM, "UserAddForm")
        else:
            form_class = UserAddForm

        return form_class


class UserUpdate(StaffPermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    slug_field = 'uuid'
    template_name = 'admin/account/user_form.html'
    permission_required = 'account.change_user'

    def get_success_url(self):
        messages.success(self.request, _('User details have been updated.'))
        return reverse('account-admin:user_list')

    def get_form_class(self):
        if hasattr(settings, 'ACCOUNT_USER_UPDATE_FORM'):
            return import_model(settings.ACCOUNT_USER_UPDATE_FORM, "UserUpdateForm")
        else:
            return UserUpdateForm

class UserDelete(StaffPermissionRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('account-admin:user_list')
    slug_field = 'uuid'
    permission_required = 'account.delete_user'
    template_name = 'admin/account/user_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, _('User has been deleted.'))
        return reverse('account-admin:user_list')


@login_required(login_url=account_settings.ADMIN_LOGIN_URL)
@sensitive_post_parameters()
def user_change_password(request, slug):
    
    if not request.user.is_superuser:
        raise PermissionDenied
    
    user = get_object_or_404(User, uuid=slug)
    
    if request.method == 'POST':
        form = UserChangePassword(user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('..')
    else:
        form = UserChangePassword(user)

    return render_to_response('admin/account/user_change_password.html', {'form':form},
        context_instance=RequestContext(request))

#########
# Group #
#########

class GroupList(StaffPermissionRequiredMixin, ListView):
    model = Group
    template_name = 'admin/account/group_list.html'
    permission_required = 'auth.change_group'

class GroupDetail(StaffPermissionRequiredMixin, DetailView):
    model = Group
    template_name = 'admin/account/group_detail.html'
    permission_required = 'auth.change_group'

class GroupCreate(StaffPermissionRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'admin/account/group_form.html'
    success_url = reverse_lazy('account-admin:group_list')
    permission_required = 'auth.add_group'

    def get_success_url(self):
        messages.success(self.request, _('Role has been created.'))
        return reverse('account-admin:group_list')

class GroupUpdate(StaffPermissionRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'admin/account/group_form.html'
    permission_required = 'auth.change_group'

    def get_success_url(self):
        messages.success(self.request, _('Role details have been updated.'))
        return reverse('account-admin:group_list')

class GroupDelete(StaffPermissionRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('account-admin:group_list')
    permission_required = 'auth.delete_group'
    template_name = 'admin/account/group_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, _('Role has been deleted.'))
        return reverse('account-admin:group_list')


########
# Docs #
########

@login_required
def docs(request):
    template = 'admin/account/docs.html'
    return render_to_response(template, {},
        context_instance=RequestContext(request))