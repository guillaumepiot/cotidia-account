from django.core.urlresolvers import reverse


def admin_menu(context):
    request = context["request"]
    return [
        {
            "text": context["SITE_NAME"],
            "url": reverse("dashboard"),
        },
        {
            "icon": "wrench",
            "align_right": True,
            "nav_items": [
                {
                    "text": "Users",
                    "url": reverse("account-admin:user_list"),
                    "permissions": ["account.add_user", "account.change_user"],
                },
                {
                    "text": "Roles",
                    "url": reverse("account-admin:group_list"),
                    "permissions": [
                        "perms.auth.add_group",
                        "perms.auth.change_group"
                    ],
                }
            ]
        },
        {
            "text": str(request.user),
            "align_right": True,
            "nav_items": [
                {
                    "text": "Profile",
                    "url": reverse("account-admin:edit"),
                    "permissions": [],
                },
                {
                    "text": "Change password",
                    "url": reverse("account-admin:password_change"),
                    "permissions": [],
                },
                {
                    "text": "Logout",
                    "url": reverse("account-admin:logout"),
                    "permissions": [],
                }
            ]
        }
    ]
