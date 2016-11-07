from django.conf.urls import include, url

urlpatterns = [
    url(r'^account/', include('cotidia.account.urls.public',
        namespace="account-public")),
    url(r'^api/account/', include('cotidia.account.urls.api',
        namespace="account-api")),
    url(r'^admin/account/', include('cotidia.account.urls.admin',
        namespace="account-admin")),
    # url(
    #     r'^admin/$',
    #     'cotidia.account.views.admin.dashboard',
    #     name="dashboard"),
    # url(r'^$', 'cotidia.account.views.public.dashboard', name="account"),
]
