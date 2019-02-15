from rest_framework import serializers

from django.urls import reverse
from django.contrib.auth.models import Group

from cotidia.admin.serializers import BaseDynamicListSerializer


class GroupAdminSerializer(BaseDynamicListSerializer):
    uuid = serializers.CharField(source="id")

    class Meta:
        model = Group
        exclude = ["id", "permissions"]

    class SearchProvider:
        display_field = "name"
        filters = ["name"]
        general_query_fields = ["name"]

    def get_endpoint(self):
        return reverse("account-api:group-list")

    def get_admin_detail_url(self, instance):
        return reverse("account-admin:group-detail", kwargs={"pk": instance.pk})
