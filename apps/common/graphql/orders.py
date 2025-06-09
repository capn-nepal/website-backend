import strawberry
import strawberry_django

from apps.common.models import (
    Event,
    GalleryItem,
    Report,
    YouTubeVideo,
)


@strawberry_django.ordering.order(Event)
class EventOrder:
    id: strawberry.auto


@strawberry_django.ordering.order(Report)
class ReportOrder:
    id: strawberry.auto


@strawberry_django.ordering.order(GalleryItem)
class GalleryItemOrder:
    id: strawberry.auto
    created_at: strawberry.auto


@strawberry_django.ordering.order(YouTubeVideo)
class YouTubeVideoOrder:
    id: strawberry.auto
    release_date: strawberry.auto
    title: strawberry.auto
