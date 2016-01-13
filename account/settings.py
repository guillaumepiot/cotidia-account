from django.conf import settings

ADMIN_LOGIN_URL = getattr(settings, 'ADMIN_LOGIN_URL', '/admin/login/')
PUBLIC_LOGIN_URL = getattr(settings, 'PUBLIC_LOGIN_URL', '/account/login/')

# Force the user to activate their account via email before being allowed 
# to login
ACCOUNT_FORCE_ACTIVATION = getattr(settings, 'ACCOUNT_FORCE_ACTIVATION', False)