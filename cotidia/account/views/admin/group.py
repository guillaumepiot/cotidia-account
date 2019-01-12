from django.contrib.auth.models import Group
from django.urls import reverse
from django.contrib import messages

from cotidia.admin.views import (
    AdminListView,
    AdminDetailView,
    AdminCreateView,
    AdminUpdateView,
    AdminDeleteView,
)
from cotidia.account.forms.admin.group import GroupAddForm, GroupUpdateForm


class GroupMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app_label"] = "account"
        return context


class GroupList(GroupMixin, AdminListView):
    columns = (("Name", "name"),)
    model = Group


class GroupDetail(GroupMixin, AdminDetailView):
    model = Group
    fieldsets = [
        {
            "legend": "Group details",
            "fields": [
                {"label": "Name", "field": "name"},
                {"label": "Permissions", "field": "permissions"},
            ],
        }
    ]

    def get_list_url(self):
        return reverse("account-admin:group-list")


class GroupCreate(GroupMixin, AdminCreateView):
    model = Group
    form_class = GroupAddForm

    def build_success_url(self):
        url_name = "{}-admin:{}-detail".format("account", self.model._meta.model_name)
        return reverse(url_name, args=[self.object.id])

    def get_list_url(self):
        return reverse("account-admin:group-list")

    def get_success_url(self):
        messages.success(self.request, "{} has been created.".format("Role"))

        return self.build_success_url()


class GroupUpdate(GroupMixin, AdminUpdateView):
    model = Group
    form_class = GroupUpdateForm

    def build_success_url(self):
        url_name = "{}-admin:{}-list".format("account", self.model._meta.model_name)
        return reverse(url_name)
        # return reverse(url_name, args=[self.get_object().id])

    def build_detail_url(self):
        url_name = "{}-admin:{}-detail".format("account", self.model._meta.model_name)
        return reverse(url_name, args=[self.get_object().id])

    def get_list_url(self):
        return reverse("account-admin:group-list")

    def get_success_url(self):
        messages.success(
            self.request,
            '{} has been updated. <a href="{}">View</a>'.format(
                "Role", self.build_detail_url()
            ),
        )

        return self.build_success_url()


class GroupDelete(GroupMixin, AdminDeleteView):
    model = Group

    def build_success_url(self):
        url_name = "{}-admin:{}-list".format("account", self.model._meta.model_name)
        return reverse(url_name)

    def get_list_url(self):
        return reverse("account-admin:group-list")

    def get_success_url(self):
        messages.success(self.request, "{} has been deleted.".format("Role"))

        return self.build_success_url()
