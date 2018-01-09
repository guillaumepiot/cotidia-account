from django.urls import path

from .views import (
    ProfileCreate,
    ProfileUpdate,
    ProfileDelete,
)

app_name = 'profile'

urlpatterns = [
    path(
        'add/<int:user_id>',
        ProfileCreate.as_view(),
        name='profile-add'
    ),
    path(
        '<int:pk>/update',
        ProfileUpdate.as_view(),
        name='profile-update'
    ),
    path(
        '<int:pk>/delete',
        ProfileDelete.as_view(),
        name='profile-delete'
    )
]
