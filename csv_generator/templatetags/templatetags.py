from django import template


register = template.Library()


@register.filter
def get_value_by_key(data, key):
    return data[key]


@register.filter
def get_unique(data):
    return list(set(data))


@register.filter
def get_unique_errors_from_formset(formset):
    unique_errors = {}

    for form in formset:
        for key, value in form.errors.items():
            if value not in unique_errors.values():
                unique_errors[key if key != "__all__" else "all"] = value
    return unique_errors
