Cotidia Account
===============

Account management for Django projects.

- Admin interface with two-factor authentication
- Public registration and login
- API for account management

Install directly from the repository:

```console
$ pip install -e git+git@code.cotidia.com:cotidia/account.git#egg=cotidia-account
```

## Settings   

Add `cotidia.account` to your INSTALLED_APPS:

```python
INSTALLED_APPS=[
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    "two_factor",

    "cotidia.core",
    "cotidia.account",
    "cotidia.mail",
    "rest_framework",
    "rest_framework.authtoken",
]
```

Middleware:

The `django_otp.middleware.OTPMiddleware` middleware must appear just after the Django auth
middleware. The `cotidia.account.middleware.AccountMiddleware` enables the two-factor authentication
enforcement if `FORCE_ADMIN_TWO_FACTOR` is `True`.

```python

MIDDLEWARE_CLASSES = (

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',

    'cotidia.account.middleware.AccountMiddleware',

)
```

Migrate the account models

```console
$ python manage.py migrate cotidia.account
```

Specify the following settings:

```python
AUTH_USER_MODEL = "account.User"
AUTHENTICATION_BACKENDS = (
    'cotidia.account.auth.EmailBackend',
)
```

By default, the login urls for the admin and the public side are set as follows:

```python
# Django defaults
LOGIN_REDIRECT_URL = '/account'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'

# Account public and admin login
ACCOUNT_ADMIN_LOGIN_URL = '/admin/account/login/'
ACCOUNT_PUBLIC_LOGIN_URL = '/account/login/'
```

Force the user to activate their account via email before being allowed to login.
`False` by default.

```python
ACCOUNT_FORCE_ACTIVATION = False
```

You can decide wether you want to allow sign up and sign in independently.
This settings will disable the URLs make the page and API hook unavailable.

```python
ACCOUNT_ALLOW_SIGN_IN = True
ACCOUNT_ALLOW_SIGN_UP = True
```

Day limit for activation link (Django settings):

```python
PASSWORD_RESET_TIMEOUT_DAYS = 3
```

Enable and force the two-factor authentication:

```python
# Change the standard one-factor authentication workflow to a two-factor
# workflow.
ENABLE_TWO_FACTOR = False
# Force all admin users to sign in using two-factor authentication.
# Only applies if `ENABLE_TWO_FACTOR` is set to `True`.
FORCE_ADMIN_TWO_FACTOR = False
```

## URLs

There's two set of urls, one for the admin management of users, role and dashboard, and one for public access.

- `admin.py` defines all the views that enable user management form an administrator perspective.
- `public.py` defines all the views for customer sign up, sign in and profile management
- `api.py` defines all the api endpoint for customer sign up, sign in and profile management

Each set can be loaded independently, under their own urls, for example:

```python
from account.views.admin import dashboard

urlpatterns = [
    url(r'^account/', include('cotidia.account.urls.public',
        namespace="account-public")),
    url(r'^api/account/', include('cotidia.account.urls.api',
        namespace="account-api")),
    url(r'^admin/account/', include('cotidia.account.urls.admin',
        namespace="account-admin")),
    url(r'^admin/$', 'cotidia.account.views.admin.dashboard', name="dashboard"),
]
```

> Please note that you must respect the url namespacing for the url reversal to work.

## Add items to the menu

You will need to register your app menu to the account menu. The register
function requires the menu name and template url.

```python
from account.menu import menu
menu.register("my_menu", "path/to/menu.html", 1)
```

Example menu (do not forget access permissions):

```html
{% load i18n %}
<div class="menu__section-header">
    {% trans "Menu header" %}
</div>
{% if perms.app.change_model %}
<a href="{% url 'admin:path_to_view' %}" class="[ menu__item ] [ menu-item ]">
    <span class="menu-item__icon fa fa-list"></span>
    <span class="menu-item__text">{% trans "My menu" %}</span>
</a>
{% endif %}
```
