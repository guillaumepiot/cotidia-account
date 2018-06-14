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

## Setup

Add `cotidia.account` to your INSTALLED_APPS:

```python
INSTALLED_APPS=[
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',

    'cotidia.core',
    'cotidia.admin',
    'cotidia.account',
    'cotidia.mail',
    'rest_framework',
    'rest_framework.authtoken',
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

Template context processor:

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [

                'cotidia.account.context_processor.account_settings',

            ],
        },
    },
]
```

Specify the user model and auth backend.


```python
AUTH_USER_MODEL = "account.User"
AUTHENTICATION_BACKENDS = (
    'cotidia.account.auth.EmailBackend',
)
```

Migrate the account models

```console
$ python manage.py migrate cotidia.account
```

## URLs

There's two set of urls, one for the admin management of users, role and dashboard, and one for public access.

- `admin.py` defines all the views that enable user management form an administrator perspective.
- `public.py` defines all the views for customer sign up, sign in and profile management
- `api.py` defines all the api endpoint for customer sign up, sign in and profile management

Each set can be loaded independently, under their own urls, for example:

```python
from django.conf.urls import url, include

from cotidia.account.views.admin import dashboard

urlpatterns = [
    path(
        'account/',
        include('cotidia.account.urls.public', namespace="account-public")
    ),
    path(
        'api/account/',
        include('cotidia.account.urls.api', namespace="account-api")
    ),
    path(
        'admin/account/',
        include('cotidia.account.urls.admin', namespace="account-admin")
    ),
    path('admin/', dashboard, name="dashboard"),
]
```

> Please note that you must respect the url namespacing for the url reversal to work.

## Django settings related to account

`LOGIN_REDIRECT_URL`

- Type: *string*
- Example: *'/account'*

Where to redirect the user if not authenticated.

`LOGIN_URL`

- Type: *string*
- Example: *'/account/login'*

The public login url specified in the account urls.

`LOGOUT_URL`

- Type: *string*
- Example: *'/account/logout'*

The public logout url specified in the account urls.

`PASSWORD_RESET_TIMEOUT_DAYS`

- Type: *int*
- Default: *3*

Day limit for activation link (Django based settings):

## Account settings

`ACCOUNT_ADMIN_LOGIN_URL`

- Type: *string*
- Example: *'/admin/account/login'*

The admin login url specified in the account urls.

`ACCOUNT_PUBLIC_LOGIN_URL`

- Type: *string*
- Example: *'/account/logout'*

The public login url specified in the account urls.

`ACCOUNT_FORCE_ACTIVATION`

- Type: *bool*
- Default: *True*

Force the user to activate their account via email before being allowed to login.

`ACCOUNT_ALLOW_SIGN_IN`

- Type: *bool*
- Default: *True*

Allow users to sign in.

`ACCOUNT_ALLOW_SIGN_UP`

- Type: *bool*
- Default: *True*

Allow users to sign up.

`ACCOUNT_ENABLE_TWO_FACTOR`

- Type: *bool*
- Default: *False*

Enable the two-factor authentication workflow.

`ACCOUNT_FORCE_ADMIN_TWO_FACTOR`

- Type: *bool*
- Default: *False*

Force the two-factor authentication workflow for staff users.

> Only applies if `ENABLE_TWO_FACTOR` is set to `True`.

`ACCOUNT_AUTO_SEND_INVITATION_EMAIL`

- Type: *bool*
- Default: *True*

Enable the automatic sending of invitation email when the user is created and
active. Also, auto send when user is updated from not active to active.
