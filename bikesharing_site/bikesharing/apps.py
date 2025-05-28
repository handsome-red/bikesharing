from django.apps import AppConfig


class BikesharingConfig(AppConfig):
    verbose_name = "Арендованный транспорт"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bikesharing'
