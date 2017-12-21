from django.conf.urls import url

from cotidia.account.views.two_factor import (
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
    url(
        regex=r'^two_factor/setup$',
        view=SetupView.as_view(),
        name='setup',
    ),
    url(
        regex=r'^two_factor/qrcode$',
        view=QRGeneratorView.as_view(),
        name='qr',
    ),
    url(
        regex=r'^two_factor/setup/complete$',
        view=SetupCompleteView.as_view(),
        name='setup_complete',
    ),
    url(
        regex=r'^two_factor/backup/tokens/list$',
        view=ListBackupTokensView.as_view(),
        name='list_backup_tokens',
    ),
    url(
        regex=r'^two_factor/backup/tokens/generate$',
        view=GenerateBackupTokensView.as_view(),
        name='generate_backup_tokens',
    ),
    url(
        regex=r'^two_factor/backup/phone/register$',
        view=PhoneSetupView.as_view(),
        name='phone_create',
    ),
    url(
        regex=r'^two_factor/backup/phone/unregister/(?P<pk>\d+)$',
        view=PhoneDeleteView.as_view(),
        name='phone_delete',
    ),
    url(
        regex=r'^two_factor$',
        view=ProfileView.as_view(),
        name='profile'
    ),
    url(
        regex=r'^two_factor/disable$',
        view=DisableView.as_view(),
        name='disable',
    ),
    url(
        regex=r'^two_factor/disable/(?P<uuid>' + ure + ')$',
        view=UserDisableView.as_view(),
        name='user-disable',
    ),
]
