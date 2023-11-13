import os
from functools import wraps

from django.conf import settings


def csv_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "csv", f"file_{instance.id}_quantity_{instance.rows}{extension}"
    )


def create_media_and_csv_folder_if_not_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        folders_to_create = ["media", "media/csv",]

        for folder in folders_to_create:
            os.makedirs(
                os.path.join(settings.BASE_DIR, folder),
                exist_ok=True
            )

        return func(*args, **kwargs)
    return wrapper


def update_dataset_status(dataset):
    dataset.status = dataset.StatusChoices.READY
    dataset.save()
