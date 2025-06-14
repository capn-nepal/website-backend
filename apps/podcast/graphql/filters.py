import strawberry
import strawberry_django

from apps.podcast.models import PodcastEpisode, PodcastSeason, VoxPopEpisode, VoxPopSeason


@strawberry_django.filters.filter(PodcastSeason, lookups=True)
class PodcastSeasonFilter:
    id: strawberry.auto
    is_archived: bool | None = strawberry.UNSET


@strawberry_django.filters.filter(PodcastEpisode, lookups=True)
class PodcastEpisodeFilter:
    id: strawberry.auto
    is_archived: bool | None = strawberry.UNSET


@strawberry_django.filters.filter(VoxPopSeason, lookups=True)
class VoxPopSeasonFilter:
    id: strawberry.auto
    title: strawberry.auto
    is_archived: bool | None = strawberry.UNSET


@strawberry_django.filters.filter(VoxPopEpisode, lookups=True)
class VoxPopEpisodeFilter:
    id: strawberry.auto
    is_archived: bool | None = strawberry.UNSET
