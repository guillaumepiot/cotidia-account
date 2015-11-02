from django.conf.urls import patterns, url

from account.api import views

urlpatterns = patterns('',
	url(r'^sign-up/$', views.SignUp.as_view(), name='sign-up'),
	url(r'^sign-in/$', views.SignIn.as_view(), name='sign-in')
)