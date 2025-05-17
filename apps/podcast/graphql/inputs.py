import strawberry
import strawberry_django

from apps.podcast.models import PodcastEpisode, PodcastSeason, VoxPop, VoxPopEpisode


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
    thumbnail: strawberry.auto


@strawberry_django.partial(PodcastEpisode)
class UpdatePodcastEpisodeInput:
    title: strawberry.auto
    podcast_season: strawberry.ID
    release_date: strawberry.auto
    episode_number: strawberry.auto
    video_url: strawberry.auto
    thumbnail: strawberry.auto


@strawberry_django.input(VoxPop)
class CreateVoxPopInput:
    title: strawberry.auto
    description: strawberry.auto
    season_number: strawberry.auto


@strawberry_django.partial(VoxPop)
class UpdateVoxPopInput:
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
    thumbnail: strawberry.auto


@strawberry_django.partial(VoxPopEpisode)
class UpdateVoxPopEpisodeInput:
    title: strawberry.auto
    voxpop_season: strawberry.ID
    release_date: strawberry.auto
    episode_number: strawberry.auto
    video_url: strawberry.auto
    thumbnail: strawberry.auto
