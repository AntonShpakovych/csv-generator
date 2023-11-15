from __future__ import annotations
from typing import List, Callable

import os
import csv

from faker import Faker

from django.conf import settings
from django.db.models.query import QuerySet

from csv_generator.models import DataSet, Column
from csv_generator.utils import (
    csv_file_path,
    create_media_and_csv_folder_if_not_exists
)


class CsvFileGeneratorService:
    def __init__(self, dataset: DataSet) -> None:
        self.dataset: DataSet = dataset
        self.rows: int = dataset.rows
        self.columns: QuerySet[Column] = dataset.schema.columns.all()
        self.faker: Faker = Faker()

    @create_media_and_csv_folder_if_not_exists
    def generate_and_save_csv(self) -> None:
        """Generate fake data, create a CSV file,
        and save it to the dataset.
        """
        file_name = csv_file_path(
            instance=self.dataset,
            filename="service.csv"
        )
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=self.dataset.schema.column_separator,
                quotechar=self.dataset.schema.string_character,
                quoting=csv.QUOTE_NONNUMERIC
            )
            writer.writerow(self._get_headers())

            for _ in range(self.rows):
                writer.writerow(self._get_rows())

        self.dataset.file = file_path
        self.dataset.save()

    def _get_headers(self) -> List[str]:
        """Generate a list of headers for the fake dataset
        based on the specified columns.
        """
        return [column.name for column in self.columns]

    def _get_rows(self) -> List[str | int]:
        """Generate a list of fake rows based on the specified columns."""
        return [
            self.__get_fake_column_value(column)
            for column in self.columns
        ]

    def __get_fake_column_value(self, column: Column) -> str | int:
        """Generate a fake value based on the specified column type."""
        column_types = {
            Column.TypeChoices.FULL_NAME: self.__get_fake_full_name,
            Column.TypeChoices.INTEGER: self.__get_fake_integer(column),
            Column.TypeChoices.COMPANY: self.__get_fake_company,
            Column.TypeChoices.JOB: self.__get_fake_job,
            Column.TypeChoices.EMAIL: self.__get_fake_email
        }

        return column_types[column.type]()

    def __get_fake_full_name(self) -> str:
        """Generate full_name through faker provider."""
        return self.faker.name()

    def __get_fake_integer(self, column: Column) -> Callable:
        """Generate integer through faker provider."""
        def random_int() -> int:
            return self.faker.random_int(
                min=column.integer_from,
                max=column.integer_to
            )
        return random_int

    def __get_fake_company(self) -> str:
        """Generate company through faker provider."""
        return self.faker.company()

    def __get_fake_job(self) -> str:
        """Generate job through faker provider."""
        return self.faker.job()

    def __get_fake_email(self) -> str:
        """Generate email through faker provider."""
        return self.faker.email()
