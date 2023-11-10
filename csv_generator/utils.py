import os


def csv_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        f"csv/file_{instance.id}_quantity_{instance.rows}{extension}"
    )
