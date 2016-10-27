from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings


__all__ = ['AccountMiddleware']


class AccountMiddleware(object):
    def process_request(self, request):

        if settings.ACCOUNT_ENABLE_TWO_FACTOR is True:

            # If the account had two factor enabled and forces admin to
            # setup the two-factor auth we then check if:
            # - They are authenticated (first step)
            # - They are not verified (second step)
            if settings.ACCOUNT_FORCE_ADMIN_TWO_FACTOR is True \
                    and request.user.is_authenticated() \
                    and not request.user.is_verified():

                setup_url = reverse('account-admin:setup')
                logout_url = reverse('account-admin:logout')
                qrcode_url = reverse('account-admin:qr')
                if request.path not in [setup_url, logout_url, qrcode_url]:
                    messages.warning(
                        request,
                        "You must setup two-factor authentication to access "
                        "the administration panel."
                        )
                    return HttpResponseRedirect(reverse('account-admin:setup'))

        return None
