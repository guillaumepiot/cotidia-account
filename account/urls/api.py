from django.conf.urls import patterns, url

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

urlpatterns += [
	
	url(r'^activate/(?P<uuid>[a-z0-9\-]+)/(?P<token>[a-z0-9\-]+)/$', 
		api.Activate.as_view(), name="activate"),
    
    url(r'^authenticate/$', 
    	api.Authenticate.as_view(), name="authenticate"),
    
    url(r'^reset-password/$', 
		api.ResetPassword.as_view(), name="reset-password"),

	url(r'^reset-password-validate/(?P<uuid>[a-z0-9\-]+)/(?P<token>[a-z0-9\-]+)/$', 
		api.ResetPasswordValidate.as_view(), name="reset-password-validate"),

	url(r'^set-password/(?P<uuid>[a-z0-9\-]+)/(?P<token>[a-z0-9\-]+)/$', 
		api.SetPassword.as_view(), name="set-password"),
	
]