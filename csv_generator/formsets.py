from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from csv_generator.models import Column, Schema
from csv_generator.forms import ColumnCreateForm


class CustomInlineFormSet(BaseInlineFormSet):
    BOOTSTRAP_SIZES = {
        "name": "col-lg-4",
        "type": "col-lg-3",
        "order": "col-lg-1",
        "integer_from": "col-lg-1",
        "integer_to": "col-lg-1",
        "DELETE": "col-lg-1"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for form in self.forms:
            form.empty_permitted = False
            self.__handle_delete(form)
        self.bootstrap_sizes = CustomInlineFormSet.BOOTSTRAP_SIZES

    @property
    def empty_form(self):
        form = super().empty_form
        self.__handle_delete(form)  # handle deleting cloned inline form

        return form

    @staticmethod
    def __handle_delete(form):
        form.fields["DELETE"].widget = forms.CheckboxInput(
            attrs={
                "onClick": "schemaDeleteColumn(this)"
            }
        )


ColumnInlineFormset = inlineformset_factory(
    parent_model=Schema,
    model=Column,
    form=ColumnCreateForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
    formset=CustomInlineFormSet,
)
