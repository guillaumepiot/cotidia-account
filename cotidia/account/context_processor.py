from cotidia.account.conf import settings


def account_settings(request):

    data = {
        "ACCOUNT_ADMIN_LOGIN_URL": settings.ACCOUNT_ADMIN_LOGIN_URL,
        "ACCOUNT_PUBLIC_LOGIN_URL": settings.ACCOUNT_PUBLIC_LOGIN_URL,
        "ACCOUNT_FORCE_ACTIVATION": settings.ACCOUNT_FORCE_ACTIVATION,
        "ACCOUNT_ENABLE_TWO_FACTOR": settings.ACCOUNT_ENABLE_TWO_FACTOR,
        "ACCOUNT_FORCE_ADMIN_TWO_FACTOR": settings.ACCOUNT_FORCE_ADMIN_TWO_FACTOR,
    }

    return data
