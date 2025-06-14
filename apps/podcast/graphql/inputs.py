import strawberry
import strawberry_django
from strawberry.file_uploads import Upload

from apps.podcast.models import (
    PodcastEpisode,
    PodcastSeason,
    VoxPopEpisode,
    VoxPopSeason,
)


@strawberry_django.input(PodcastSeason)
class CreatePodcastSeasonInput:
    title: strawberry.auto
    description: strawberry.auto
    season_number: strawberry.auto


@strawberry_django.partial(PodcastSeason)
class UpdatePodcastSeasonInput:
    title: strawberry.auto
    description: strawberry.auto
    season_number: strawberry.auto


@strawberry_django.input(PodcastEpisode)
class CreatePodcastEpisodeInput:
    title: strawberry.auto
    podcast_season: strawberry.ID
    release_date: strawberry.auto
    episode_number: strawberry.auto
    video_url: strawberry.auto
    thumbnail: Upload


@strawberry_django.partial(PodcastEpisode)
class UpdatePodcastEpisodeInput:
    title: strawberry.auto
    podcast_season: strawberry.ID
    release_date: strawberry.auto
    episode_number: strawberry.auto
    video_url: strawberry.auto
    thumbnail: Upload | None = strawberry.UNSET


@strawberry_django.input(VoxPopSeason)
class CreateVoxPopSeasonInput:
    title: strawberry.auto
    description: strawberry.auto
    season_number: strawberry.auto


@strawberry_django.partial(VoxPopSeason)
class UpdateVoxPopSeasonInput:
    title: strawberry.auto
    description: strawberry.auto
    season_number: strawberry.auto


@strawberry_django.input(VoxPopEpisode)
class CreateVoxPopEpisodeInput:
    title: strawberry.auto
    voxpop_season: strawberry.ID
    release_date: strawberry.auto
    episode_number: strawberry.auto
    video_url: strawberry.auto
    thumbnail: Upload


@strawberry_django.partial(VoxPopEpisode)
class UpdateVoxPopEpisodeInput:
    title: strawberry.auto
    voxpop_season: strawberry.ID
    release_date: strawberry.auto
    episode_number: strawberry.auto
    video_url: strawberry.auto
    thumbnail: Upload | None = strawberry.UNSET
