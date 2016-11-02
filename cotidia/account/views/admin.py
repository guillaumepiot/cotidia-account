from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404, resolve_url
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.db.models import Q
from cotidia.account.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.http import is_safe_url

from cotidia.account.models import User
from cotidia.account.user_forms import (
    UserAddForm,
    UserUpdateForm,
    GroupForm,
    ProfileForm,
    UserChangePassword
    )
from cotidia.account.utils import StaffPermissionRequiredMixin, import_model


@sensitive_post_parameters()
@csrf_protect
def login_remember_me(
        request,
        authentication_form=None,
        template_name='admin/account/login.html',
        *args,
        **kwargs):
    """Custom login view that enables "remember me" functionality."""

    if request.user.is_authenticated():
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


########
# User #
########

class UserList(StaffPermissionRequiredMixin, ListView):
    model = User
    template_name = 'admin/account/user_list.html'
    permission_required = 'account.change_user'
    paginate_by = 25

    def get_queryset(self):
        # Get filter params
        is_staff = self.request.GET.get('is_staff')
        search_query = self.request.GET.get('query')

        query = User.objects.filter()

        if is_staff:
            query = query.filter(is_staff=is_staff)

        if search_query:
            q_split = search_query.split(' ')
            for q in q_split:
                query = query.filter(
                    Q(first_name__icontains=q) |
                    Q(last_name__icontains=q) |
                    Q(email__icontains=q)
                    )

        return query


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
            form_class = import_model(
                settings.ACCOUNT_USER_ADD_FORM, "UserAddForm"
                )
        else:
            form_class = UserAddForm

        return form_class


class UserUpdate(StaffPermissionRequiredMixin, UpdateView):
    model = User
    slug_field = 'uuid'
    template_name = 'admin/account/user_form.html'
    permission_required = 'account.change_user'

    def check_user(self, user):
        if not user.is_superuser and self.get_object().is_superuser:
            return False
        else:
            return True

    def get_success_url(self):
        messages.success(self.request, _('User details have been updated.'))
        return reverse('account-admin:user_list')

    def get_form_class(self):
        return self.kwargs.get('user_form') or UserUpdateForm


class UserDelete(StaffPermissionRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('account-admin:user_list')
    slug_field = 'uuid'
    permission_required = 'account.delete_user'
    template_name = 'admin/account/user_confirm_delete.html'

    def check_user(self, user):
        if not user.is_superuser and self.get_object().is_superuser:
            return False
        else:
            return True

    def get_success_url(self):
        messages.success(self.request, _('User has been deleted.'))
        return reverse('account-admin:user_list')


@login_required(login_url=settings.ACCOUNT_ADMIN_LOGIN_URL)
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

    template = 'admin/account/user_change_password.html'

    return render(request, template, {'form': form})


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
    return render(request, template)
