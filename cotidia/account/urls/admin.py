"""
Re-definition of Django's auth URLs.

This is done for convenience. It allows us to save all registration and auth
related templates in the same `/templates/registration/` folder.

"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from cotidia.account.conf import settings

from cotidia.account.forms import (
    EmailAuthenticationForm,
    AccountPasswordResetForm,
    AccountSetPasswordForm,
    AccountPasswordChangeForm
    )
from cotidia.account.views.admin import (
    dashboard,
    edit,
    login_remember_me,
    UserList,
    UserCreate,
    UserDetail,
    UserUpdate,
    UserDelete,
    user_change_password,
    GroupList,
    GroupCreate,
    GroupDetail,
    GroupUpdate,
    GroupDelete,
    docs
)

from cotidia.account.views.two_factor import (
    LoginView,
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
    url(r'^$', dashboard, name="dashboard"),
    url(r'profile/edit/$', edit, name="edit"),
    url(
        r'^logout/$',
        auth_views.logout,
        {'template_name': 'admin/account/logout.html'},
        name='logout',
    ),
    url(
        r'^password/change/$',
        auth_views.password_change,
        {
            'template_name': 'admin/account/password_change_form.html',
            'password_change_form': AccountPasswordChangeForm,
            'post_change_redirect': 'done/'
        },
        name='password_change',
    ),
    url(
        r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'admin/account/password_change_done.html'},
        name='password_change_done',
    ),
    url(
        r'^password/reset/$',
        auth_views.password_reset,
        {
            'template_name': 'admin/account/password_reset_form.html',
            'post_reset_redirect': 'account-admin:password_reset_done',
            'password_reset_form': AccountPasswordResetForm,
            'email_template_name': 'admin/account/password_reset_email.html',
            'subject_template_name': 'admin/account/password_reset_subject.txt'
        },
        name='password_reset',
    ),
    url(
        r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'admin/account/password_reset_confirm.html',
            'set_password_form': AccountSetPasswordForm,
            'post_reset_redirect': 'account-admin:password_reset_complete'
        },
        name='password_reset_confirm',
    ),
    url(
        r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {
            'template_name': 'admin/account/password_reset_complete.html',
        },
        name='password_reset_complete',
    ),
    url(
        r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'admin/account/password_reset_done.html'},
        name='password_reset_done',
    ),
    url(r'^user/$', UserList.as_view(), name='user_list'),
    url(r'^user/add/$', UserCreate.as_view(), name='user_add'),
    url(
        r'^user/(?P<slug>[0-9a-z\-]+)/$',
        UserDetail.as_view(),
        name='user_detail'),
    url(
        r'^user/(?P<slug>[0-9a-z\-]+)/update$',
        UserUpdate.as_view(),
        name='user_update'),
    url(
        r'^user/(?P<slug>[0-9a-z\-]+)/delete/$',
        UserDelete.as_view(),
        name='user_delete'),
    url(
        r'^user/(?P<slug>[0-9a-z\-]+)/change-password/$',
        user_change_password,
        name='user_change_password'),
    url(
        r'^role/$',
        GroupList.as_view(),
        name='group_list'),
    url(
        r'^role/add/$',
        GroupCreate.as_view(),
        name='group_add'),
    url(
        r'^role/(?P<pk>[\d]+)/$',
        GroupDetail.as_view(),
        name='group_detail'),
    url(
        r'^role/(?P<pk>[\d]+)/update$',
        GroupUpdate.as_view(),
        name='group_update'),
    url(
        r'^role/(?P<pk>[\d]+)/delete/$',
        GroupDelete.as_view(),
        name='group_delete'),
    url(
        r'^docs/$',
        docs,
        name='docs'),
]

if settings.ACCOUNT_ENABLE_TWO_FACTOR is True:
    # Two factor auth pattern
    urlpatterns += [
        url(
            regex=r'^login/$',
            view=LoginView.as_view(),
            name='login',
        ),
        url(
            regex=r'^two_factor/setup/$',
            view=SetupView.as_view(),
            name='setup',
        ),
        url(
            regex=r'^two_factor/qrcode/$',
            view=QRGeneratorView.as_view(),
            name='qr',
        ),
        url(
            regex=r'^two_factor/setup/complete/$',
            view=SetupCompleteView.as_view(),
            name='setup_complete',
        ),
        url(
            regex=r'^two_factor/backup/tokens/list/$',
            view=ListBackupTokensView.as_view(),
            name='list_backup_tokens',
        ),
        url(
            regex=r'^two_factor/backup/tokens/generate/$',
            view=GenerateBackupTokensView.as_view(),
            name='generate_backup_tokens',
        ),
        url(
            regex=r'^two_factor/backup/phone/register/$',
            view=PhoneSetupView.as_view(),
            name='phone_create',
        ),
        url(
            regex=r'^two_factor/backup/phone/unregister/(?P<pk>\d+)/$',
            view=PhoneDeleteView.as_view(),
            name='phone_delete',
        ),
        url(
            regex=r'^two_factor/$',
            view=ProfileView.as_view(),
            name='profile'
        ),
        url(
            regex=r'^two_factor/disable/$',
            view=DisableView.as_view(),
            name='disable',
        ),
        url(
            regex=r'^two_factor/disable/(?P<uuid>'+ure+')$',
            view=UserDisableView.as_view(),
            name='user-disable',
        ),
    ]
else:
    urlpatterns += [
        url(
            r'^login/$',
            login_remember_me,
            {'template_name': 'admin/account/login.html',
             'authentication_form': EmailAuthenticationForm, },
            name='login',
        ),
    ]
