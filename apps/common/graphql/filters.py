import strawberry
import strawberry_django

from apps.common.models import (
    Event,
    GalleryItem,
    ImageTypeEnum,
    Report,
    StatusEnum,
    YouTubeVideo,
)


@strawberry_django.filters.filter(Event, lookups=True)
class EventFilter:
    id: strawberry.auto
    is_deleted: bool | None


@strawberry_django.filters.filter(Report, lookups=True)
class ReportFilter:
    id: strawberry.auto
    status: StatusEnum
    is_deleted: bool | None


@strawberry_django.filters.filter(GalleryItem, lookups=True)
class GalleryItemFilter:
    id: strawberry.auto
    image_type: ImageTypeEnum | None


@strawberry_django.filters.filter(YouTubeVideo, lookups=True)
class YouTubeVideoFilter:
    id: strawberry.auto
    title: strawberry.auto
    is_archived: bool | None
