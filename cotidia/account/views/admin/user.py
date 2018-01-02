import django_filters

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from cotidia.admin.views import (
    AdminListView,
    AdminDetailView,
    AdminCreateView,
    AdminUpdateView,
    AdminDeleteView,
)
from cotidia.account.models import User
from cotidia.account.forms.admin.user import (
    UserAddForm,
    UserUpdateForm,
    UserChangePasswordForm,
    UserInviteForm
)


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        label="Search",
        method="search"
    )

    class Meta:
        model = User
        fields = ['first_name']

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )


class UserList(AdminListView):
    columns = (
        ('Name', 'name'),
        ('Email', 'email'),
        ('Superuser', 'is_superuser'),
        ('Staff', 'is_staff'),
        ('Active', 'is_active'),
        ('Date Joined', 'date_joined'),

    )
    model = User
    row_click_action = "detail"
    row_actions = ['view']
    filterset = UserFilter


class UserDetail(AdminDetailView):
    model = User
    fieldsets = [
        {
            "legend": "User details",
            "fields": [
                [
                    {
                        "label": "Name",
                        "field": "name",
                    },
                    {
                        "label": "Email",
                        "field": "email",
                    }
                ],
                [
                    {
                        "label": "Username",
                        "field": "username",
                    }
                ]
            ]
        },
        {
            "legend": "Roles & Permissions",
            "fields": [
                [
                    {
                        "label": "Active",
                        "field": "is_active",
                    },
                    {
                        "label": "Staff",
                        "field": "is_staff",
                    },
                    {
                        "label": "Superuser",
                        "field": "is_superuser",
                    }
                ],
                {
                    "label": "Roles",
                    "field": "groups",
                },
                {
                    "label": "Permissions",
                    "field": "user_permissions",
                }
            ]
        },
        # {
        #     "legend": "People",
        #     "template_name": "admin/team/team/people.html"
        # }
    ]


class UserCreate(AdminCreateView):
    model = User
    form_class = UserAddForm

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.object.is_active:
            self.object.send_invitation_email()

        return response


class UserUpdate(AdminUpdateView):
    model = User
    form_class = UserUpdateForm

    def form_valid(self, form):
        previous_instance = self.get_object()
        response = super().form_valid(form)

        # If `is_active` change state from False to True, send the invitation
        if not previous_instance.is_active and self.object.is_active:
            # Only send if the user was never invited
            if not self.object.password:
                self.object.send_invitation_email()

        return response


class UserInvite(AdminUpdateView):
    model = User
    form_class = UserInviteForm

    def get_template_names(self):
        return ["admin/account/user/invite.html"]

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.object.is_active and not self.object.password:
            self.object.send_invitation_email()

        return response

    def get_success_url(self):
        messages.success(
            self.request,
            '{} has been invited. <a href="{}">View</a>'.format(
                self.model._meta.verbose_name,
                self.build_detail_url()
            )
        )
        return self.build_success_url()


class UserDelete(AdminDeleteView):
    model = User


class UserChangePassword(AdminUpdateView):
    model = User
    form_class = UserChangePasswordForm

    def check_user(self, user):
        """Superuser only."""
        if user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() == request.user:
            return HttpResponseRedirect(
                reverse('account-admin:password-change')
            )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        del kwargs['instance']
        kwargs['user'] = self.get_object()
        return kwargs
