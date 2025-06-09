import strawberry
import strawberry_django

from apps.podcast.models import (
    PodcastEpisode,
    PodcastSeason,
    VoxPopEpisode,
    VoxPopSeason,
)


@strawberry_django.type(PodcastSeason)
class PodcastSeasonType:
    id: strawberry.ID
    title: strawberry.auto
    season_number: strawberry.auto
    description: strawberry.auto


@strawberry_django.type(PodcastEpisode)
class PodcastEpisodeType:
    id: strawberry.ID
    podcast_season: strawberry.auto
    release_date: strawberry.auto
    episode_number: strawberry.auto
    title: strawberry.auto
    video_url: strawberry.auto
    thumbnail: strawberry.auto
    is_archived: strawberry.auto


@strawberry_django.type(VoxPopSeason)
class VoxPopSeasonType:
    id: strawberry.ID
    title: strawberry.auto
    season_number: strawberry.auto
    description: strawberry.auto


@strawberry_django.type(VoxPopEpisode)
class VoxPopEpisodeType:
    id: strawberry.ID
    voxpop_season: strawberry.auto
    release_date: strawberry.auto
    episode_number: strawberry.auto
    title: strawberry.auto
    video_url: strawberry.auto
    thumbnail: strawberry.auto
    is_archived: strawberry.auto
