from django.conf.urls import url

from cotidia.account.views.admin.group import (
    GroupList,
    GroupCreate,
    GroupDetail,
    GroupUpdate,
    GroupDelete
)


ure = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    url(
        r'^$',
        GroupList.as_view(),
        name='group-list'),
    url(
        r'^add/$',
        GroupCreate.as_view(),
        name='group-add'),
    url(
        r'^(?P<pk>[\d]+)$',
        GroupDetail.as_view(),
        name='group-detail'),
    url(
        r'^(?P<pk>[\d]+)/update$',
        GroupUpdate.as_view(),
        name='group-update'),
    url(
        r'^(?P<pk>[\d]+)/delete$',
        GroupDelete.as_view(),
        name='group-delete'),
]
