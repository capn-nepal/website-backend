from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "news_type", "status")
    search_fields = ("title",)
    list_filter = ("news_type", "status")
