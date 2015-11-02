"""
Re-definition of Django's auth URLs.

This is done for convenience. It allows us to save all registration and auth
related templates in the same `/templates/registration/` folder.

"""
from django.conf.urls import url, patterns
from django.contrib.auth import views as auth_views

from account.forms import (
    EmailAuthenticationForm, 
    AccountPasswordResetForm, 
    AccountSetPasswordForm, 
    AccountPasswordChangeForm)
from account.views.public import dashboard, login_remember_me, edit, sign_up, activate

urlpatterns = patterns(
    '',
    url(r'^$', dashboard, name="dashboard"),
    url(r'^edit/$', edit, name="edit"),
    url(r'^sign-up/$', sign_up, name='sign-up',),
    url(
        r'^login/$',
        login_remember_me,
        {'template_name': 'account/login.html',
         'authentication_form': EmailAuthenticationForm, },
        name='login',
    ),
    url(
        r'^activate/(?P<uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/(?P<token>.+)/$',
        activate,
        {'template_name': 'account/activate.html'},
        name='activate',
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'template_name': 'account/logout.html'},
        name='logout',
    ),
    url(
        r'^password/change/$',
        auth_views.password_change,
        {'template_name': 'account/password_change_form.html',
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
        {'template_name': 'account/password_reset_form.html',
            'post_reset_redirect': 'account-public:password_reset_done',
            'password_reset_form': AccountPasswordResetForm,
            'email_template_name': 'account/password_reset_email.html',
            'subject_template_name': 'account/password_reset_subject.txt',},
        name='password_reset',
    ),
    url(
        r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'account/password_reset_confirm.html',
            'post_reset_redirect': 'account-public:password_reset_complete',
            'set_password_form':AccountSetPasswordForm
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
    ),
)
