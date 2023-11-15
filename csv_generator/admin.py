from django.contrib import admin

from csv_generator.models import Column, Schema, DataSet


class ColumnInline(admin.TabularInline):
    model = Column


class SchemaAdmin(admin.ModelAdmin):
    inlines = [ColumnInline]


admin.site.register(Schema, SchemaAdmin)
admin.site.register(DataSet)
admin.site.register(Column)
