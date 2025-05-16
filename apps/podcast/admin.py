from django.contrib import admin

from .models import PodcastEpisode, PodcastSeason, VoxPop, VoxPopEpisode


@admin.register(PodcastSeason)
class PodcastSeasonAdmin(admin.ModelAdmin):
    list_display = ("title", "season_number")
    list_filter = ("season_number",)
    search_fields = ("title", "season_number")


@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ("title", "podcast_season", "episode_number", "release_date", "video_url")
    list_filter = ("episode_number", "release_date")
    search_fields = ("title", "podcast_season")


@admin.register(VoxPop)
class VoxPopAdmin(admin.ModelAdmin):
    list_display = ("title", "season_number")
    list_filter = ("season_number",)
    search_fields = ("title", "season_number")


@admin.register(VoxPopEpisode)
class VoxPopEpisodeAdmin(admin.ModelAdmin):
    list_display = ("title", "voxpop_season", "episode_number", "release_date", "video_url")
    list_filter = ("episode_number", "release_date")
    search_fields = ("title", "voxpop_season")
