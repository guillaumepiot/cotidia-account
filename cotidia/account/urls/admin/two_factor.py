from django.urls import path

from cotidia.account.views.admin.two_factor import (
    ProfileView,
    DisableView,
    UserDisableView,
    ListBackupTokensView,
    GenerateBackupTokensView,
    SetupView,
    SetupCompleteView,
    PhoneDeleteView,
    PhoneSetupView
)
from two_factor.views import (
    QRGeneratorView
)

ure = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


urlpatterns = [
    path(
        'setup',
        SetupView.as_view(),
        name='setup',
    ),
    path(
        'qrcode',
        QRGeneratorView.as_view(),
        name='qr',
    ),
    path(
        'setup/complete',
        SetupCompleteView.as_view(),
        name='setup_complete',
    ),
    path(
        'backup/tokens/list',
        ListBackupTokensView.as_view(),
        name='list_backup_tokens',
    ),
    path(
        'backup/tokens/generate',
        GenerateBackupTokensView.as_view(),
        name='generate_backup_tokens',
    ),
    path(
        'backup/phone/register',
        PhoneSetupView.as_view(),
        name='phone_create',
    ),
    path(
        'backup/phone/unregister/<pk>',
        PhoneDeleteView.as_view(),
        name='phone_delete',
    ),
    path(
        '',
        ProfileView.as_view(),
        name='profile'
    ),
    path(
        'disable',
        DisableView.as_view(),
        name='disable',
    ),
    path(
        'disable/<uuid>',
        UserDisableView.as_view(),
        name='user-disable',
    ),
]
