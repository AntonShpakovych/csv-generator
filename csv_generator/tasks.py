from django.shortcuts import get_object_or_404

from config.celery import app

from csv_generator.models import DataSet
from csv_generator.utils import update_dataset_status
from csv_generator.services.csv_file_generator_service import (
    CsvFileGeneratorService
)


@app.task(bind=True, max_retries=3, soft_time_limit=300)
def produce_csv_and_update_status(self, dataset_pk):
    try:
        dataset = get_object_or_404(DataSet, pk=dataset_pk)
        service_csv = CsvFileGeneratorService(dataset=dataset)

        service_csv.generate_and_save_csv()
        update_dataset_status(dataset=dataset)
    except Exception as e:
        raise self.retry(exc=e)
