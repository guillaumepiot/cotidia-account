from django.conf import settings

ADMIN_LOGIN_URL = getattr(settings, 'ADMIN_LOGIN_URL', '/admin/login/')
PUBLIC_LOGIN_URL = getattr(settings, 'PUBLIC_LOGIN_URL', '/account/login/')