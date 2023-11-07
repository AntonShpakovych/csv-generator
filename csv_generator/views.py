from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import mixins

from csv_generator.models import Schema
from csv_generator.forms import SchemaCreateForm
from csv_generator.formsets import ColumnInlineFormset


class SchemaListView(mixins.LoginRequiredMixin, generic.ListView):
    """List view for schema created by an authorized user"""
    model = Schema
    context_object_name = "schemas"
    paginate_by = 13

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)


class SchemaUpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = Schema
    form_class = SchemaCreateForm
    success_url = reverse_lazy("csv_generator:schema-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = kwargs.get(
            "formset"
        ) or ColumnInlineFormset(
            instance=self.object
        )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        formset = ColumnInlineFormset(request.POST, instance=self.object)
        form = self.get_form()

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset=formset)
        return self.form_invalid(form, formset=formset)

    def form_valid(self, form, **kwargs):
        self.object = form.save()
        formset = kwargs.get("formset")

        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        formset = kwargs.get("formset")

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class SchemaCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    """Create view with additional formsets for `columns`"""
    model = Schema
    form_class = SchemaCreateForm
    success_url = reverse_lazy("csv_generator:schema-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = kwargs.get("formset") or ColumnInlineFormset()

        return context

    def post(self, request, *args, **kwargs):
        self.object = None

        formset = ColumnInlineFormset(request.POST)
        form = self.get_form()

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset=formset)
        return self.form_invalid(form, formset=formset)

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user
        self.object = form.save()

        formset = kwargs.get("formset")

        formset.instance = self.object
        formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        formset = kwargs.get("formset")

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class SchemaDeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    """Delete schema created by an authorized user without confirmation"""
    model = Schema
    success_url = reverse_lazy("csv_generator:schema-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not obj.user == self.request.user:
            raise Http404("Schema doesn't exist")
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())
