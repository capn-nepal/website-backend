from django.contrib import admin

from .models import (
    Artwork,
    Event,
    EventAsset,
    Gallery,
    GalleryItem,
    Report,
    YouTubeVideo,
)


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
    list_display = ("title", "published_date", "status")
    list_filter = ("id", "title")
    search_fields = ("title", "status")


@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "video_url", "is_archived")
    list_filter = ("id", "title")
    search_fields = ("title", "is_archived")


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_archived")
    search_fields = ("name",)


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("caption", "image", "is_archived", "gallery")
    autocomplete_fields = ("gallery",)
    list_select_related = ["gallery"]


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("name", "image")
