import datetime

import strawberry
import strawberry_django

from apps.common.models import (
    Artwork,
    Event,
    EventAsset,
    Gallery,
    GalleryItem,
    Report,
    YouTubeVideo,
)
from apps.user.graphql.types import UserType


# -- Interfaces
@strawberry.interface
class UserResourceTypeMixin:
    created_at: datetime.datetime
    modified_at: datetime.datetime

    created_by: UserType
    modified_by: UserType


@strawberry_django.type(Event)
class EventType:
    id: strawberry.ID
    name: strawberry.auto
    location: strawberry.auto
    start_date: strawberry.auto
    end_date: strawberry.auto
    description: strawberry.auto


@strawberry_django.type(EventAsset)
class EventAssetType:
    id: strawberry.ID
    event: EventType
    image: strawberry.auto


@strawberry_django.type(Report)
class ReportType:
    id: strawberry.ID
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    report_file: strawberry.auto
    status: strawberry.auto
    cover_image: strawberry.auto


@strawberry_django.type(Gallery)
class GalleryType:
    id: strawberry.ID
    name: strawberry.auto
    description: strawberry.auto
    is_archived: strawberry.auto


@strawberry_django.type(GalleryItem)
class GalleryItemType:
    id: strawberry.auto
    image: strawberry.auto
    gallery: GalleryType
    caption: strawberry.auto
    is_archived: strawberry.auto


@strawberry_django.type(YouTubeVideo)
class YouTubeVideoType:
    id: strawberry.ID
    title: strawberry.auto
    video_url: strawberry.auto
    thumbnail: strawberry.auto
    release_date: strawberry.auto
    is_archived: strawberry.auto


@strawberry_django.type(Artwork)
class ArtworkType:
    id: strawberry.ID
    name: strawberry.auto
    image: strawberry.auto
