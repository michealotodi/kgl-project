from django.apps import AppConfig


class KglappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kglapp'


class KglappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kglapp'

    def ready(self):
        import kglapp.signals  # Import signals here
