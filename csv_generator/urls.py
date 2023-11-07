from django.urls import path

from csv_generator.views import (
    SchemaListView,
    SchemaCreateView,
    SchemaDeleteView,
    SchemaUpdateView
)


urlpatterns = [
    path(
        "schemas/",
        SchemaListView.as_view(),
        name="schema-list"
    ),
    path(
        "schemas/create/",
        SchemaCreateView.as_view(),
        name="schema-create",
    ),
    path(
        "schemas/<int:pk>/delete/",
        SchemaDeleteView.as_view(),
        name="schema-delete"
    ),
    path(
        "schemas/<int:pk>/update/",
        SchemaUpdateView.as_view(),
        name="schema-update"
    )
]

app_name = "csv_generator"
