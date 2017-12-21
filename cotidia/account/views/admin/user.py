import django_filters

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    UserChangePasswordForm
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


class UserUpdate(AdminUpdateView):
    model = User
    form_class = UserUpdateForm


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

# @login_required(login_url=settings.ACCOUNT_ADMIN_LOGIN_URL)
# @sensitive_post_parameters()
# def user_change_password(request, pk):

#     if not request.user.is_superuser:
#         raise PermissionDenied

#     user = get_object_or_404(User, pk=pk)

#     if user == request.user:
#         return HttpResponseRedirect(reverse('account-admin:password-change'))

#     if request.method == 'POST':
#         form = UserChangePassword(user, request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('..')
#     else:
#         form = UserChangePassword(user)

#     template = 'admin/account/user_change_password.html'

#     return render(request, template, {'form': form})
