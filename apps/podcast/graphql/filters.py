import strawberry
import strawberry_django

from apps.podcast.models import PodcastEpisode, PodcastSeason, VoxPop, VoxPopEpisode


@strawberry_django.filters.filter(PodcastSeason, lookups=True)
class PodcastSeasonFilter:
    id: strawberry.auto
    title: strawberry.auto


@strawberry_django.filters.filter(PodcastEpisode, lookups=True)
class PodcastEpisodeFilter:
    id: strawberry.auto
    is_archived: bool


@strawberry_django.filters.filter(VoxPop, lookups=True)
class VoxPopFilter:
    id: strawberry.auto
    title: strawberry.auto


@strawberry_django.filters.filter(VoxPopEpisode, lookups=True)
class VoxPopEpisodeFilter:
    id: strawberry.auto
    is_archived: bool
