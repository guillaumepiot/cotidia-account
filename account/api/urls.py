from django.conf.urls import patterns, url

from account.api import views
from account import settings as account_settings

urlpatterns = []

if account_settings.ACCOUNT_ALLOW_SIGN_IN:
    urlpatterns += [
        url(r'^sign-in/$', views.SignIn.as_view(), name='sign-in')
    ]

if account_settings.ACCOUNT_ALLOW_SIGN_UP:
    urlpatterns += [
        url(r'^sign-up/$', views.SignUp.as_view(), name='sign-up')
    ]

urlpatterns += [
    url(r'^authenticate/$', views.Authenticate.as_view(), name="authenticate")
]
