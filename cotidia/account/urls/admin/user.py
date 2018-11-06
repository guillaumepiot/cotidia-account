from django.conf.urls import url
from django.urls import path

from cotidia.account.views.admin.user import (
    UserList,
    UserListAdmin,
    UserCreate,
    UserDetail,
    UserUpdate,
    UserDelete,
    UserChangePassword,
    UserInvite
)

ure = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    url(
        r'^$',
        UserList.as_view(),
        name='user-list'
    ),
    url(
        r'^admin$',
        UserListAdmin.as_view(),
        name='user-list-admin'
    ),
    url(
        r'^add$',
        UserCreate.as_view(),
        name='user-add'
    ),
    path(
        '<pk>',
        UserDetail.as_view(),
        name='user-detail'
    ),
    url(
        r'^(?P<pk>[\d]+)/update$',
        UserUpdate.as_view(),
        name='user-update'
    ),
    url(
        r'^(?P<pk>[\d]+)/invite$',
        UserInvite.as_view(),
        name='user-invite'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete$',
        UserDelete.as_view(),
        name='user-delete'
    ),
    url(
        r'^(?P<pk>[\d]+)/change-password$',
        UserChangePassword.as_view(),
        name='user-change-password'
    ),
]
