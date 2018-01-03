from django.conf.urls import url

from .views import (
    ProfileCreate,
    ProfileUpdate,
    ProfileDelete,
)

urlpatterns = [
    url(
        r'^add/(?P<user_id>[\d]+)$',
        ProfileCreate.as_view(),
        name='profile-add'
    ),
    url(
        r'^(?P<pk>[\d]+)/update$',
        ProfileUpdate.as_view(),
        name='profile-update'
    ),
    url(
        r'^(?P<pk>[\d]+)/delete$',
        ProfileDelete.as_view(),
        name='profile-delete'
    )
]
