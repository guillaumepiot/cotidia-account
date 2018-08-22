from django.conf.urls import url
from django.contrib.auth import views as auth_views
from cotidia.account.conf import settings

from cotidia.account.forms import (
    AccountPasswordResetForm,
    AccountSetPasswordForm,
    AccountPasswordChangeForm)
from cotidia.account.views.public import (
    dashboard,
    LoginView,
    LogoutView,
    edit,
    sign_up,
    activate,
    activation_pending,
    resend_activation_link,
    InviteView
)

u_re = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

app_name = 'cotidia.account'

urlpatterns = [
    url(r'^$', dashboard, name="dashboard"),
    url(r'^edit/$', edit, name="edit"),
    url(
        r'^activate/(?P<uuid>'+u_re+')/(?P<token>.+)$',
        activate,
        {'template_name': 'account/activate.html'},
        name='activate',
    ),
    url(
        r'^activation-pending/(?P<uuid>'+u_re+')$',
        activation_pending,
        {'template_name': 'account/activation-pending.html'},
        name="activation-pending"),
    url(
        r'^resend-activation-link/(?P<uuid>'+u_re+')$',
        resend_activation_link,
        name='resend-activation-link',
    ),
    url(
        r'^logout/$',
        LogoutView.as_view(),
        name='logout',
    ),
    url(
        r'^password/change/$',
        auth_views.password_change,
        {
            'template_name': 'account/password_change_form.html',
            'post_change_redirect': 'account-public:password_change_done',
            'password_change_form': AccountPasswordChangeForm},
        name='password_change',
    ),
    url(
        r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'account/password_change_done.html'},
        name='password_change_done',
    ),
    url(
        r'^password/reset/$',
        auth_views.password_reset,
        {
            'template_name': 'account/password_reset_form.html',
            'post_reset_redirect': 'account-public:password_reset_done',
            'password_reset_form': AccountPasswordResetForm,
            'email_template_name': 'account/password_reset_email.html',
            'subject_template_name': 'account/password_reset_subject.txt'
        },
        name='password_reset',
    ),
    url(
        r'^invite/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        InviteView.as_view(),
        name='invite',
    ),
    url(
        r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'account/password_reset_confirm.html',
            'post_reset_redirect': 'account-public:password_reset_complete',
            'set_password_form': AccountSetPasswordForm
        },
        name='password_reset_confirm',
    ),
    url(
        r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'account/password_reset_complete.html'},
        name='password_reset_complete',
    ),
    url(
        r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'account/password_reset_done.html'},
        name='password_reset_done',
    )
]

if settings.ACCOUNT_ALLOW_SIGN_IN:
    urlpatterns += [
        url(
            r'^sign-in/$',
            LoginView.as_view(),
            name='sign-in',
        ),
    ]

if settings.ACCOUNT_ALLOW_SIGN_UP:
    urlpatterns += [
        url(r'^sign-up/$', sign_up, name='sign-up'),
    ]
