from django.urls import path

from csv_generator.views import (
    SchemaListView,
    SchemaCreateView,
    SchemaDeleteView,
    SchemaUpdateView,
    SchemaGenerateCSVView,
    SchemaDatasetStatusView,
    SchemaDataSetDownloadCSVFileView
)


urlpatterns = [
    path(
        "",
        SchemaListView.as_view(),
        name="schema-list"
    ),
    path(
        "create/",
        SchemaCreateView.as_view(),
        name="schema-create",
    ),
    path(
        "<int:pk>/delete/",
        SchemaDeleteView.as_view(),
        name="schema-delete"
    ),
    path(
        "<int:pk>/update/",
        SchemaUpdateView.as_view(),
        name="schema-update"
    ),
    path(
        "<int:pk>/generate_csv/",
        SchemaGenerateCSVView.as_view(),
        name="schema-generate-csv"
    ),
    path(
        "datasets/<int:pk>/status/",
        SchemaDatasetStatusView.as_view(),
        name="dataset-status"
    ),
    path(
        "datasets/<int:pk>/download-csv/",
        SchemaDataSetDownloadCSVFileView.as_view(),
        name="dataset-download-csv"
    )
]

app_name = "csv_generator"
