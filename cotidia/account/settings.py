from django.conf import settings

ADMIN_LOGIN_URL = getattr(settings, 'ADMIN_LOGIN_URL', '/admin/login/')
PUBLIC_LOGIN_URL = getattr(settings, 'PUBLIC_LOGIN_URL', '/account/login/')

# Force the user to activate their account via email before being allowed
# to login
ACCOUNT_FORCE_ACTIVATION = getattr(settings, 'ACCOUNT_FORCE_ACTIVATION', True)

ACCOUNT_ALLOW_SIGN_IN = getattr(settings, 'ACCOUNT_ALLOW_SIGN_IN', True)
ACCOUNT_ALLOW_SIGN_UP = getattr(settings, 'ACCOUNT_ALLOW_SIGN_UP', True)

# Change the standard one-factor authentication workflow to a two-factor
# workflow.
ACCOUNT_ENABLE_TWO_FACTOR = getattr(
    settings, 'ACCOUNT_ENABLE_TWO_FACTOR', False)
# Force all admin users to sign in using two-factor authentication.
# Only applies if `ACCOUNT_ENABLE_TWO_FACTOR` is set to `True`.
ACCOUNT_FORCE_ADMIN_TWO_FACTOR = getattr(
    settings, 'ACCOUNT_FORCE_ADMIN_TWO_FACTOR', False)
