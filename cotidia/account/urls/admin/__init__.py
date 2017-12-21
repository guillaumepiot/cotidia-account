from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from cotidia.account.views.two_factor import (
    LoginView
)
from cotidia.account.views.admin import login_remember_me
from cotidia.account.forms import EmailAuthenticationForm
from cotidia.account.conf import settings
from cotidia.account.forms import (
    AccountPasswordResetForm,
    AccountSetPasswordForm,
    AccountPasswordChangeForm
)
from cotidia.account.views.admin import (
    dashboard,
    edit
)


ure = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^$', dashboard, name="dashboard"),
    url(r'user/', include('cotidia.account.urls.admin.user')),
    url(r'role/', include('cotidia.account.urls.admin.group')),

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
        name='password-change',
    ),
    url(
        r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'admin/account/password_change_done.html'},
        name='password-change-done',
    ),
    url(
        r'^password/reset/$',
        auth_views.password_reset,
        {
            'template_name': 'admin/account/password_reset_form.html',
            'post_reset_redirect': 'account-admin:password-reset-done',
            'password_reset_form': AccountPasswordResetForm,
            'email_template_name': 'admin/account/password_reset_email.html',
            'subject_template_name': 'admin/account/password_reset_subject.txt'
        },
        name='password-reset',
    ),
    url(
        r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'admin/account/password_reset_confirm.html',
            'set_password_form': AccountSetPasswordForm,
            'post_reset_redirect': 'account-admin:password-reset-complete'
        },
        name='password-reset-confirm',
    ),
    url(
        r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {
            'template_name': 'admin/account/password_reset_complete.html',
        },
        name='password-reset-complete',
    ),
    url(
        r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'admin/account/password_reset_done.html'},
        name='password-reset-done',
    ),
]

if settings.ACCOUNT_ENABLE_TWO_FACTOR is True:
    # Two factor auth pattern
    urlpatterns += [
        url(r'two-factor/', include('cotidia.account.urls.admin.two_factor')),
        url(
            regex=r'^login$',
            view=LoginView.as_view(),
            name='login',
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
