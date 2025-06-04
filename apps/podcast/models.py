from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import UserResource


class PodcastSeason(UserResource):
    title = models.CharField(max_length=100, verbose_name=_("Podcast Title"))
    description = models.TextField(blank=True)
    season_number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.title


class PodcastEpisode(UserResource):
    podcast_season = models.ForeignKey(PodcastSeason, on_delete=models.PROTECT, related_name="episodes")
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, verbose_name=_("Episode Title"))
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    release_date = models.DateTimeField(verbose_name=_("Episode Release Date"))
    is_archived = models.BooleanField(default=False)

    class Meta:  # type: ignore[reportAssignmentType]
        unique_together = ["podcast_season", "episode_number"]

    def __str__(self):
        return self.title


class VoxPopSeason(UserResource):
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description = models.TextField(blank=True)
    season_number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.title


class VoxPopEpisode(UserResource):
    voxpop_season = models.ForeignKey(VoxPopSeason, on_delete=models.PROTECT)
    episode_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, verbose_name=_("Episode Title"))
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    release_date = models.DateTimeField(verbose_name=_("Episode Release Date"))
    is_archived = models.BooleanField(default=False)

    class Meta:  # type: ignore[reportAssignmentType]
        unique_together = ["voxpop_season", "episode_number"]

    def __str__(self):
        return self.title
