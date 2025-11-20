from django.apps import AppConfig


class CarsdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carsdb'

    def ready(self):
        import carsdb.signals  # Регистрируем сигналы