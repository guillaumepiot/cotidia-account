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
        },
        {
            "text": str(request.user),
            "icon": "user",
            "align_right": True,
            "nav_items": [
                {
                    "text": "Profile",
                    "icon": "id-card",
                    "url": reverse("account-admin:edit"),
                    "permissions": [],
                },
                {
                    "text": "Change password",
                    "icon": "key",
                    "url": reverse("account-admin:password-change"),
                    "permissions": [],
                },
                {
                    "text": "Logout",
                    "icon": "sign-out",
                    "url": reverse("account-admin:logout"),
                    "permissions": [],
                }
            ]
        }
    ]
