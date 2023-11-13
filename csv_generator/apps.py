from django.apps import AppConfig
from django.core.signals import setting_changed


class CsvGeneratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "csv_generator"

    def ready(self):
        from csv_generator.signals import create_random_csv_file

        setting_changed.connect(create_random_csv_file)
