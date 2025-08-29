import strawberry
import strawberry_django

from apps.common.models import (
    Changemaker,
    Event,
    Gallery,
    GalleryItem,
    Report,
    StatusEnum,
    YouTubeVideo,
)


@strawberry_django.filters.filter(Event, lookups=True)
class EventFilter:
    id: strawberry.auto
    is_deleted: bool | None = strawberry.UNSET


@strawberry_django.filters.filter(Report, lookups=True)
class ReportFilter:
    id: strawberry.auto
    status: StatusEnum | None = strawberry.UNSET


@strawberry_django.filters.filter(YouTubeVideo, lookups=True)
class YouTubeVideoFilter:
    id: strawberry.auto
    title: strawberry.auto
    is_archived: bool | None = strawberry.UNSET


@strawberry_django.filters.filter(Gallery, lookups=True)
class GalleryFilter:
    is_archived: bool | None = strawberry.UNSET


@strawberry_django.filters.filter(GalleryItem, lookups=True)
class GalleryItemFilter:
    is_archived: bool | None = strawberry.UNSET


@strawberry_django.filters.filter(Changemaker, lookups=True)
class ChangemakerFilter:
    is_archived: bool | None = strawberry.UNSET
