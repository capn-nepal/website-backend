import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated

from .filters import (
    EventFilter,
    GalleryFilter,
    GalleryItemFilter,
    ReportFilter,
    YouTubeVideoFilter,
)
from .orders import (
    ArtworkOrder,
    EventOrder,
    GalleryItemOrder,
    GalleryOrder,
    ReportOrder,
    YouTubeVideoOrder,
)
from .types import (
    ArtworkType,
    EventAssetType,
    EventType,
    GalleryItemType,
    GalleryType,
    ReportType,
    YouTubeVideoType,
)


@strawberry.type
class Query:
    # event-----------------------
    events: OffsetPaginated[EventType] = strawberry_django.offset_paginated(
        order=EventOrder,
        filters=EventFilter,
        extensions=[],
    )
    event: EventType = strawberry_django.field(extensions=[])

    event_assets: OffsetPaginated[EventAssetType] = strawberry_django.offset_paginated(
        extensions=[],
    )
    event_asset: EventAssetType = strawberry_django.field(extensions=[])
    # report------------------
    reports: OffsetPaginated[ReportType] = strawberry_django.offset_paginated(
        order=ReportOrder,
        filters=ReportFilter,
        extensions=[],
    )
    report: ReportType = strawberry_django.field(extensions=[])

    # images ----------------------------

    galleries: OffsetPaginated[GalleryType] = strawberry_django.offset_paginated(
        order=GalleryOrder,
        filters=GalleryFilter,
        extensions=[],
    )

    gallery: GalleryType = strawberry_django.field(extensions=[])

    gallery_items: OffsetPaginated[GalleryItemType] = strawberry_django.offset_paginated(
        order=GalleryItemOrder,
        filters=GalleryItemFilter,
        extensions=[],
    )
    gallery_item: GalleryItemType = strawberry_django.field(extensions=[])

    art_works: OffsetPaginated[ArtworkType] = strawberry_django.offset_paginated(
        order=ArtworkOrder,
        extensions=[],
    )
    art_work: ArtworkType = strawberry_django.field(extensions=[])

    # youtube videos -------------------------------------------
    youtube_videos: OffsetPaginated[YouTubeVideoType] = strawberry_django.offset_paginated(
        filters=YouTubeVideoFilter,
        order=YouTubeVideoOrder,
        extensions=[],
    )
    youtube_video: YouTubeVideoType = strawberry_django.field(extensions=[])
