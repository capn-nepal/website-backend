import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsAuthenticated

from .filters import PodcastEpisodeFilter, PodcastSeasonFilter, VoxPopEpisodeFilter, VoxPopFilter
from .orders import PodcastEpisodeOrder, PodcastSeasonOrder, VoxPopEpisodeOrder, VoxPopOrder
from .types import PodcastEpisodeType, PodcastSeasonType, VoxPopEpisodeType, VoxPopSeasonType


@strawberry.type
class Query:
    # podcast --------------------------
    podcast_seasons: OffsetPaginated[PodcastSeasonType] = strawberry_django.offset_paginated(
        order=PodcastSeasonOrder,
        filters=PodcastSeasonFilter,
        extensions=[IsAuthenticated()],
    )
    podcast_season: PodcastSeasonType = strawberry_django.field(extensions=[])
    # podcast Episode --------------------------
    podcast_episodes: OffsetPaginated[PodcastEpisodeType] = strawberry_django.offset_paginated(
        order=PodcastEpisodeOrder,
        filters=PodcastEpisodeFilter,
        extensions=[IsAuthenticated()],
    )

    podcast_episode: PodcastEpisodeType = strawberry_django.field(extensions=[])

    # VoxPop ---------------------------------
    voxpop_seasons: OffsetPaginated[VoxPopSeasonType] = strawberry_django.offset_paginated(
        order=VoxPopOrder,
        filters=VoxPopFilter,
        extensions=[IsAuthenticated()],
    )
    voxpop_season: VoxPopSeasonType = strawberry_django.field(extensions=[])

    # VoxPop Episode --------------------------------
    voxpop_episodes: OffsetPaginated[VoxPopEpisodeType] = strawberry_django.offset_paginated(
        order=VoxPopEpisodeOrder,
        filters=VoxPopEpisodeFilter,
        extensions=[IsAuthenticated()],
    )

    voxpop_episode: VoxPopEpisodeType = strawberry_django.field(extensions=[])
