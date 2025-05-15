from django.contrib import admin

from .models import Event, EventAsset, Report


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "location", "is_deleted")
    search_fields = ("name", "location")
    list_filter = ("start_date", "location")


@admin.register(EventAsset)
class EventAssetsAdmin(admin.ModelAdmin):
    list_display = ("id", "event")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "status", "is_deleted")
    list_filter = ("id", "title")
    search_fields = ("title", "status")
