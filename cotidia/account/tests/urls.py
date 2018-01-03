from django.conf.urls import include, url

from cotidia.account.views.admin import dashboard


urlpatterns = [
    url(r'^account/', include('cotidia.account.urls.public',
        namespace='account-public')),
    url(r'^api/account/', include('cotidia.account.urls.api',
        namespace='account-api')),
    url(r'^admin/account/', include('cotidia.account.urls.admin',
        namespace='account-admin')),
    url(r'^admin/profile/', include('cotidia.account.tests.profile.urls',
        namespace='profile-admin')),
    url(r'^admin/mail/', include('cotidia.mail.urls',
        namespace='mail-admin')),
    url(
        r'^admin/$',
        dashboard,
        name='dashboard'
    ),
    # url(r'^$', 'cotidia.account.views.public.dashboard', name="account"),
]
