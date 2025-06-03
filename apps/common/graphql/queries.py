import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsAuthenticated

from .filters import (
    EventFilter,
    GalleryItemFilter,
    ReportFilter,
    YouTubeVideoFilter,
)
from .orders import (
    EventOrder,
    GalleryItemOrder,
    ReportOrder,
    YouTubeVideoOrder,
)
from .types import (
    EventAssetType,
    EventType,
    GalleryItemType,
    ReportType,
    YouTubeVideoType,
)


@strawberry.type
class Query:
    # event-----------------------
    events: OffsetPaginated[EventType] = strawberry_django.offset_paginated(
        order=EventOrder,
        filters=EventFilter,
        extensions=[IsAuthenticated()],
    )
    event: EventType = strawberry_django.field(extensions=[IsAuthenticated()])

    event_assets: OffsetPaginated[EventAssetType] = strawberry_django.offset_paginated(
        extensions=[IsAuthenticated()],
    )
    event_asset: EventAssetType = strawberry_django.field(extensions=[IsAuthenticated()])
    # report------------------
    reports: OffsetPaginated[ReportType] = strawberry_django.offset_paginated(
        order=ReportOrder,
        filters=ReportFilter,
        extensions=[IsAuthenticated()],
    )
    report: ReportType = strawberry_django.field(extensions=[IsAuthenticated()])

    # images ----------------------------
    gallery_items: OffsetPaginated[GalleryItemType] = strawberry_django.offset_paginated(
        filters=GalleryItemFilter,
        order=GalleryItemOrder,
        extensions=[IsAuthenticated()],
    )
    gallery_item: GalleryItemType = strawberry_django.field(extensions=[IsAuthenticated()])

    # youtube videos -------------------------------------------
    youtube_videos: OffsetPaginated[YouTubeVideoType] = strawberry_django.offset_paginated(
        filters=YouTubeVideoFilter,
        order=YouTubeVideoOrder,
        extensions=[IsAuthenticated()],
    )
    youtube_video: YouTubeVideoType = strawberry_django.field(extensions=[IsAuthenticated()])
