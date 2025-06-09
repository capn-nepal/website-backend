import strawberry
import strawberry_django

from apps.podcast.models import PodcastEpisode, PodcastSeason, VoxPopEpisode, VoxPopSeason


@strawberry_django.ordering.order(PodcastSeason)
class PodcastSeasonOrder:
    id: strawberry.auto


@strawberry_django.ordering.order(PodcastEpisode)
class PodcastEpisodeOrder:
    id: strawberry.auto


@strawberry_django.ordering.order(VoxPopSeason)
class VoxPopOrder:
    id: strawberry.auto


@strawberry_django.ordering.order(VoxPopEpisode)
class VoxPopEpisodeOrder:
    id: strawberry.auto
