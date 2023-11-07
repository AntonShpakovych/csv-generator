from django import forms

from csv_generator.models import Schema, Column


class SchemaCreateForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ["name", "column_separator", "string_character"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "column_separator": forms.Select(attrs={"class": "form-select"}),
            "string_character": forms.Select(attrs={"class": "form-select"}),
        }


class ColumnCreateForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ["name", "order", "type", "integer_to", "integer_from"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                },
            ),
            "order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "integer_to": forms.NumberInput(
                attrs={
                    "class": "form-control column-integer_to",
                }
            ),
            "integer_from": forms.NumberInput(
                attrs={
                    "class": "form-control column-integer_from",
                }
            ),
            "type": forms.Select(
                attrs={
                    "onChange": "schemaOptionalColumnInputOnChange(this)",
                    "class": "form-select"
                },
                choices=Column.TypeChoices.choices,
            )
        }
        labels = {
            "integer_to": "To",
            "integer_from": "From"
        }
