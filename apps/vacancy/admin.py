from django.contrib import admin

from .models import JobVacancy, Position


@admin.register(JobVacancy)
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ("position", "deadline", "number_of_vacancies")
    list_filter = ("deadline",)
    search_fields = ("position",)
    autocomplete_fields = ("position",)
    list_select_related = ["position"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "employment_type")
    list_filter = ("name", "employment_type")
    search_fields = ("name", "employment_type")
