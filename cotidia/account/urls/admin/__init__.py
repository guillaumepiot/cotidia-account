from django.conf.urls import url
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

from cotidia.account.views.admin.two_factor import TwoFactorLoginView
from cotidia.account.forms import EmailAuthenticationForm
from cotidia.account.conf import settings
from cotidia.account.forms import (
    AccountPasswordResetForm,
    AccountSetPasswordForm,
    AccountPasswordChangeForm,
)
from cotidia.account.views.admin import dashboard, edit


ure = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

app_name = "cotidia.account"

urlpatterns = [
    url(r"^$", dashboard, name="dashboard"),
    url(r"user/", include("cotidia.account.urls.admin.user")),
    url(r"role/", include("cotidia.account.urls.admin.group")),
    url(r"profile/edit/$", edit, name="edit"),
    url(
        r"^logout/$",
        LogoutView.as_view(template_name="admin/account/logout.html"),
        name="logout",
    ),
    url(
        r"^password/change/$",
        PasswordChangeView.as_view(
            template_name="admin/account/password_change_form.html",
            form_class=AccountPasswordChangeForm,
            success_url=reverse_lazy("account-admin:password-change-done"),
        ),
        name="password-change",
    ),
    url(
        r"^password/change/done/$",
        PasswordChangeDoneView.as_view(
            template_name="admin/account/password_change_done.html"
        ),
        name="password-change-done",
    ),
    url(
        r"^password/reset/$",
        PasswordResetView.as_view(
            template_name="admin/account/password_reset_form.html",
            success_url=reverse_lazy("account-admin:password-reset-done"),
            form_class=AccountPasswordResetForm,
            email_template_name="admin/account/password_reset_email.html",
            subject_template_name="admin/account/password_reset_subject.txt",
        ),
        name="password-reset",
    ),
    url(
        r"^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        PasswordResetConfirmView.as_view(
            template_name="admin/account/password_reset_confirm.html",
            form_class=AccountSetPasswordForm,
            success_url=reverse_lazy("account-admin:password-reset-complete"),
        ),
        name="password-reset-confirm",
    ),
    url(
        r"^password/reset/complete/$",
        PasswordResetCompleteView.as_view(
            template_name="admin/account/password_reset_complete.html"
        ),
        name="password-reset-complete",
    ),
    url(
        r"^password/reset/done/$",
        PasswordResetDoneView.as_view(
            template_name="admin/account/password_reset_done.html"
        ),
        name="password-reset-done",
    ),
]

if settings.ACCOUNT_ENABLE_TWO_FACTOR is True:
    # Two factor auth pattern
    urlpatterns += [
        path("two-factor/", include("cotidia.account.urls.admin.two_factor")),
        path("login", TwoFactorLoginView.as_view(), name="login"),
    ]
else:
    urlpatterns += [
        path(
            "login",
            LoginView.as_view(
                template_name="admin/account/login.html",
                form_class=EmailAuthenticationForm,
            ),
            name="login",
        )
    ]
