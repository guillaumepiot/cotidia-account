from django.conf.urls import url

from account.views import api
from account import settings as account_settings

urlpatterns = []

if account_settings.ACCOUNT_ALLOW_SIGN_IN:
    urlpatterns += [
        url(r'^sign-in/$', api.SignIn.as_view(), name='sign-in')
    ]

if account_settings.ACCOUNT_ALLOW_SIGN_UP:
    urlpatterns += [
        url(r'^sign-up/$', api.SignUp.as_view(), name='sign-up')
    ]

ure = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns += [
    url(
        r'^activate/(?P<uuid>'+ure+')/(?P<token>[a-z0-9\-]+)/$',
        api.Activate.as_view(),
        name="activate"),
    url(
        r'^authenticate/$',
        api.Authenticate.as_view(),
        name="authenticate"),
    url(
        r'^reset-password/$',
        api.ResetPassword.as_view(),
        name="reset-password"),
    url(
        r'^reset-password-validate/(?P<uuid>'+ure+')/(?P<token>[a-z0-9\-]+)/$',
        api.ResetPasswordValidate.as_view(),
        name="reset-password-validate"),
    url(
        r'^set-password/(?P<uuid>'+ure+')/(?P<token>[a-z0-9\-]+)/$',
        api.SetPassword.as_view(),
        name="set-password"),
    url(
        r'^update-details/$',
        api.UpdateDetails.as_view(),
        name="update-details"),
]
