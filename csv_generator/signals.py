from django.db.models.signals import post_save
from django.dispatch import receiver

from csv_generator.models import DataSet
from csv_generator.services.csv_file_generator_service import (
    CsvFileGeneratorService
)
from csv_generator.utils import update_dataset_status


@receiver(post_save, sender=DataSet)
def create_random_csv_file(sender, instance, created, **kwargs):
    if created:
        csv_service = CsvFileGeneratorService(dataset=instance)
        csv_service.generate_and_save_csv()
        update_dataset_status(dataset=instance)
