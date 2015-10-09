Cotidia Account
=================

Generic account management (admin & public) for Django applications.

The package has dependencies:

- Django==1.8.4
- django-form-utils==1.0.3


All those dependencies will get automatically installed when the package is 
installed.

    $ pip install -e git+git@bitbucket.org:guillaumepiot/cotidia-account.git#egg=account


## Settings

Add 'account' to your INSTALLED_APPS:

    INSTALLED_APPS = (
        ...
        'account',
        ...
    )

Specify the following settings:

    AUTH_USER_MODEL = 'account.User'
    
    AUTHENTICATION_BACKENDS = (
        'account.auth.EmailBackend',
    )

By default, the login urls for the admin and the public side are set as follows:

    ADMIN_LOGIN_URL = '/admin/login/'
    PUBLIC_LOGIN_URL = '/account/login/'

Those settings can be overridden in `settings.py` if required.

## URLs

There's two set of urls, one for the admin management of users, role and dashboard, and one for public access.

- `admin.py` defines all the views that enable user managenemt form an administrator perspective.
- `public.py` defines all the views for customer sign up, sign in and profile management

Each set can be loaded independently, under their own urls, for example:

    urlpatterns = [
        url(r'^admin/account/', include('account.urls.admin', 
            namespace="account-admin")),
        url(r'^account/', include('account.urls.public', 
            namespace="account-public")),
    ]

## User models override

On a project basis, you may want to add your own fields to the user models.
You can override which model class is used on a project basis by declaring a 
path to another `User` model class.

    ACCOUNT_USER_MODEL = "my_project.models"

In your `models.py` file, create your own `User` class:

    from account.models import BaseUser

    class User(BaseUser):
        # My fields
        #...

        class Meta:
            abstract = True
            db_table = 'account_user'

The model must be an abstract, and the table name set as account_user.