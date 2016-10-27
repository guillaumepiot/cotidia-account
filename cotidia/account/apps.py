from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = "cotidia.account"
    label = "account"

    def ready(self):
        import cotidia.account.signals
