from django.urls import path
from django.conf.urls import url

from cotidia.account.views import api
from cotidia.account.serializers.group import GroupAdminSerializer
from cotidia.admin.views.api import DynamicListAPIView

ure = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

app_name = "cotidia.account"

urlpatterns = [
    url(r"^sign-in$", api.SignIn.as_view(), name="sign-in"),
    url(r"^sign-up$", api.SignUp.as_view(), name="sign-up"),
    url(
        r"^activate/(?P<uuid>" + ure + ")/(?P<token>[a-z0-9\-]+)$",
        api.Activate.as_view(),
        name="activate",
    ),
    url(
        r"^resend-activation-link/(?P<uuid>" + ure + ")$",
        api.ResendActivationLink.as_view(),
        name="resend-activation-link",
    ),
    url(r"^authenticate$", api.Authenticate.as_view(), name="authenticate"),
    url(r"^reset-password$", api.ResetPassword.as_view(), name="reset-password"),
    url(
        r"^reset-password-validate/(?P<uuid>" + ure + ")/(?P<token>[a-z0-9\-]+)$",
        api.ResetPasswordValidate.as_view(),
        name="reset-password-validate",
    ),
    url(
        r"^set-password/(?P<uuid>" + ure + ")/(?P<token>[a-z0-9\-]+)$",
        api.SetPassword.as_view(),
        name="set-password",
    ),
    url(r"^update-details$", api.UpdateDetails.as_view(), name="update-details"),
    url(r"^change-password$", api.ChangePassword.as_view(), name="change-password"),
    path(
        "dynamic-list/auth/group",
        DynamicListAPIView.as_view(permission_required=["auth.change_group"]),
        {
            "app_label": "auth",
            "model": "group",
            "serializer_class": GroupAdminSerializer,
        },
        name="group-list",
    ),
]
