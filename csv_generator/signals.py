from django.db.models.signals import post_save
from django.dispatch import receiver

from csv_generator.models import DataSet
from csv_generator.tasks import produce_csv_and_update_status


@receiver(post_save, sender=DataSet)
def create_random_csv_file(sender, instance, created, **kwargs):
    if created:
        produce_csv_and_update_status.delay(dataset_pk=instance.pk)
