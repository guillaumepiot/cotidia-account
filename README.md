Cotidia Account
=================

Generic account management (admin & public) for Django applications.

The package has dependencies:

- Django==1.8.4
- django-form-utils==1.0.3


All those dependencies will get automatically installed when the package is 
installed.

    $ pip install -e git+git@bitbucket.org:guillaumepiot/cotidia-account.git#egg=account

Make your migrations (project basis):

    $ python manage.py makemigrations account


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
    
    LOGIN_REDIRECT_URL = '/account'
    LOGIN_URL = '/account/login/'
    LOGOUT_URL = '/account/logout/'

    ADMIN_LOGIN_URL = '/admin/login/'
    PUBLIC_LOGIN_URL = '/account/login/'

Force the user to activate their account via email before being allowed to login.
`False` by default.

    ACCOUNT_FORCE_ACTIVATION = False

Those settings can be overridden in `settings.py` if required.

## URLs

There's two set of urls, one for the admin management of users, role and dashboard, and one for public access.

- `admin.py` defines all the views that enable user managenemt form an administrator perspective.
- `public.py` defines all the views for customer sign up, sign in and profile management

Each set can be loaded independently, under their own urls, for example:
    
    from account.views.admin import dashboard

    urlpatterns = [
        url(r'^admin/account/', include('account.urls.admin', 
            namespace="account-admin")),
        url(r'^account/', include('account.urls.public', 
            namespace="account-public")),
        url(r'^admin/$', dashboard, name="dashboard"),
    ]

## User models override

On a project basis, you may want to add your own fields to the user models.
You can override which model class is used on a project basis by declaring a 
path to another `User` model class.

    AUTH_USER_MODEL = "account.User"
    ACCOUNT_USER_MODEL = "my_project.models"

In your `models.py` file, create your own `User` class:

    from django.db import models

    class User(object):
        title = models.CharField(max_length=100, choices=settings.USER_TITLE, blank=True, null=True)
        company_name = models.CharField('Company name', max_length=100, blank=True, null=True)

        #Phones
        phone_number = models.CharField(max_length=100, blank=True, null=True)
        mobile_number = models.CharField(max_length=100, blank=True, null=True)
        fax_number = models.CharField(max_length=100, blank=True, null=True)

        # Special instructions
        special_instructions = models.TextField('Special instructions', max_length=1000, blank=True, null=True)

        def __unicode__(self):
            if self.first_name or self.last_name:
                return '%s %s' % (self.first_name, self.last_name)
            return self.username

The model is only a standard Python object, it will get merged into a full User 
model in the account models section on load.

## Add items to the menu

You will need to register your app menu to the account menu. The register 
function requires the menu name and template url.

    from account.menu import menu
    menu.register("my_menu", "path/to/menu.html", 1) #Number is order id

Example menu (do not forget access permissions):

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