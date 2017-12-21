from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

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
        context['app_label'] = 'account'
        return context


class GroupList(GroupMixin, AdminListView):
    columns = (
        ('Name', 'name'),
    )
    model = Group


class GroupDetail(GroupMixin, AdminDetailView):
    model = Group
    fieldsets = [
        {
            "legend": "Group details",
            "fields": [
                {
                    "label": "Name",
                    "field": "name",
                },
                {
                    "label": "Permissions",
                    "field": "permissions",
                }
            ]
        },
        # {
        #     "legend": "People",
        #     "template_name": "admin/team/team/people.html"
        # }
    ]


class GroupCreate(GroupMixin, AdminCreateView):
    model = Group
    form_class = GroupAddForm

    def build_success_url(self):
        url_name = "{}-admin:{}-detail".format(
            'account',
            self.model._meta.model_name
        )
        return reverse(url_name, args=[self.object.id])


class GroupUpdate(GroupMixin, AdminUpdateView):
    model = Group
    form_class = GroupUpdateForm

    def build_success_url(self):
        url_name = "{}-admin:{}-list".format(
            'account',
            self.model._meta.model_name
        )
        return reverse(url_name)
        # return reverse(url_name, args=[self.get_object().id])

    def build_detail_url(self):
        url_name = "{}-admin:{}-detail".format(
            'account',
            self.model._meta.model_name
        )
        return reverse(url_name, args=[self.get_object().id])


class GroupDelete(GroupMixin, AdminDeleteView):
    model = Group

    def build_success_url(self):
        url_name = "{}-admin:{}-list".format(
            'account',
            self.model._meta.model_name
        )
        return reverse(url_name)
