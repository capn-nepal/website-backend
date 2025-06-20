import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated

from .filters import PodcastEpisodeFilter, PodcastSeasonFilter, VoxPopEpisodeFilter, VoxPopSeasonFilter
from .orders import PodcastEpisodeOrder, PodcastSeasonOrder, VoxPopEpisodeOrder, VoxPopOrder
from .types import PodcastEpisodeType, PodcastSeasonType, VoxPopEpisodeType, VoxPopSeasonType


@strawberry.type
class Query:
    # podcast --------------------------
    podcast_seasons: OffsetPaginated[PodcastSeasonType] = strawberry_django.offset_paginated(
        order=PodcastSeasonOrder,
        filters=PodcastSeasonFilter,
        extensions=[],
    )
    podcast_season: PodcastSeasonType = strawberry_django.field(extensions=[])
    # podcast Episode --------------------------
    podcast_episodes: OffsetPaginated[PodcastEpisodeType] = strawberry_django.offset_paginated(
        order=PodcastEpisodeOrder,
        filters=PodcastEpisodeFilter,
        extensions=[],
    )

    podcast_episode: PodcastEpisodeType = strawberry_django.field(extensions=[])

    # VoxPop ---------------------------------
    voxpop_seasons: OffsetPaginated[VoxPopSeasonType] = strawberry_django.offset_paginated(
        order=VoxPopOrder,
        filters=VoxPopSeasonFilter,
        extensions=[],
    )
    voxpop_season: VoxPopSeasonType = strawberry_django.field(extensions=[])

    # VoxPop Episode --------------------------------
    voxpop_episodes: OffsetPaginated[VoxPopEpisodeType] = strawberry_django.offset_paginated(
        order=VoxPopEpisodeOrder,
        filters=VoxPopEpisodeFilter,
        extensions=[],
    )

    voxpop_episode: VoxPopEpisodeType = strawberry_django.field(extensions=[])
