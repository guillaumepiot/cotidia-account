from django.urls import reverse


def admin_menu(context):
    request = context["request"]
    return [
        {
            "icon": "wrench",
            "text": "Settings",
            "align_right": True,
            "nav_items": [
                {
                    "text": "Users",
                    "url": reverse("account-admin:user-list"),
                    "permissions": ["account.add_user", "account.change_user"],
                },
                {
                    "text": "Roles",
                    "url": reverse("account-admin:group-list"),
                    "permissions": [
                        "perms.auth.add_group",
                        "perms.auth.change_group"
                    ],
                }
            ]
        }
    ]
