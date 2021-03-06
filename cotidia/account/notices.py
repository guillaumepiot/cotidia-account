from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cotidia.mail.notice import Notice


class NewUserActivationNotice(Notice):
    name = "New user activation"
    identifier = "new-user-activation"
    html_template = "account/notices/new_user_activation.html"
    text_template = "account/notices/new_user_activation.txt"
    subject = "account/notices/new_user_activation_subject.txt"

    default_context = {
        "url": "url",
        "firstname": "Guillaume",
        "SITE_URL": settings.SITE_URL,
        "SITE_NAME": settings.SITE_NAME,
        "DEBUG": settings.DEBUG,
    }


class ResetPasswordNotice(Notice):
    name = "Reset password"
    identifier = "reset-password"
    html_template = "account/notices/reset_password.html"
    text_template = "account/notices/reset_password.txt"
    subject = u"%s" % _("Password reset")

    default_context = {
        "url": "url",
        "firstname": "Guillaume",
        "SITE_URL": settings.SITE_URL,
        "SITE_NAME": settings.SITE_NAME,
        "DEBUG": settings.DEBUG,
    }


class UserInvitationNotice(Notice):
    name = "User invitation"
    identifier = "user-invitation"
    html_template = "account/notices/invitation.html"
    text_template = "account/notices/invitation.txt"
    subject = "Welcome"

    default_context = {
        "url": "url",
        "firstname": "Guillaume",
        "SITE_URL": settings.SITE_URL,
        "SITE_NAME": settings.SITE_NAME,
        "DEBUG": settings.DEBUG,
    }
