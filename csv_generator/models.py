from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from csv_generator.utils import csv_file_path


class Schema(models.Model):
    class ColumnSeparatorChoices(models.TextChoices):
        COMMA = ",", _("Comma")
        SPACE = " ", _("Space")
        SEMICOLON = ";", _("Semicolon")
        VERTICAL_LINE = "|", _("Vertical line")
        SLASH = "/", _("Slash")

    class StringCharacterChoices(models.TextChoices):
        DOUBLE_QUOTES = '"', _("Double quotes")
        SINGLE_QUOTES = "'", _("Single quotes")
        TRIPLE_QUOTES = '"""', _("Triple quotes")

    name = models.CharField(max_length=255, unique=True)
    column_separator = models.CharField(
        max_length=1,
        choices=ColumnSeparatorChoices.choices,
        default=ColumnSeparatorChoices.COMMA
    )
    string_character = models.CharField(
        max_length=3,
        choices=StringCharacterChoices.choices,
        default=StringCharacterChoices.SINGLE_QUOTES
    )
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="schemas"
    )

    def __str__(self) -> str:
        return f"Schema: id={self.id} name={self.name}"

    class Meta:
        ordering = ["name"]


class DataSet(models.Model):
    class StatusChoices(models.TextChoices):
        PROCESSING = "processing", _("Processing")
        READY = "ready", _("Ready")

    rows = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(
                1,
                message="Rows must be greater than or equal to 1"
            )
        ]
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PROCESSING
    )
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name="datasets"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=csv_file_path, null=True, blank=True)

    def __str__(self) -> str:
        return f"<DataSet: id={self.id} schema={self.schema}>"

    class Meta:
        ordering = ["-status"]


class Column(models.Model):
    class TypeChoices(models.TextChoices):
        FULL_NAME = "full_name", _("Full name")
        INTEGER = "integer", _("Integer")
        Company = "company", _("Company")
        JOB = "job", _("Job")
        EMAIL = "email", _("Email")

    name = models.CharField(max_length=255)
    order = models.IntegerField()
    type = models.CharField(
        max_length=9,
        choices=TypeChoices.choices,
        default=TypeChoices.INTEGER
    )
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name="columns",
    )

    # optional parameters for integer type
    integer_from = models.IntegerField(null=True, blank=True)
    integer_to = models.IntegerField(null=True, blank=True)

    def validate_integer(self):
        if self.type == Column.TypeChoices.INTEGER:
            if not self.integer_to:
                raise ValidationError(
                    {
                        "integer_to": "If column data type integer, "
                                      "integer_to required"
                    }
                )
            elif not self.integer_from:
                raise ValidationError(
                    {
                        "integer_from": "If column data type integer, "
                                        "integer_from required"
                    }
                )
            elif self.integer_from > self.integer_to:
                raise ValidationError(
                    {
                        "integer_from": "Integer from should be "
                                        "greater than integer to"
                    }
                )

    def clean(self):
        self.validate_integer()

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return (
            f"<Column: id={self.id} "
            f"name={self.name} "
            f"schema={self.schema}>"
        )

    class Meta:
        unique_together = [
            ["name", "schema"],
            ["schema", "order"],
        ]
        ordering = ["order"]
