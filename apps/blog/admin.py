from django.contrib import admin

from .models import Blog, BlogAsset


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "featured")
    search_fields = ("title", "author")
    list_filter = ("published_date", "featured")


@admin.register(BlogAsset)
class BlogAssetsAdmin(admin.ModelAdmin):
    list_display = ("id", "blog")
