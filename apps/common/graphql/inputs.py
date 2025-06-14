import strawberry
import strawberry_django
from strawberry.file_uploads import Upload

from apps.common.models import (
    Event,
    EventAsset,
    GalleryItem,
    ImageTypeEnum,
    Report,
    YouTubeVideo,
)


@strawberry_django.input(Event)
class CreateEventInput:
    name: strawberry.auto
    description: strawberry.auto
    location: strawberry.auto
    start_date: strawberry.auto
    end_date: strawberry.auto


@strawberry_django.partial(Event)
class UpdateEventInput:
    name: strawberry.auto
    description: strawberry.auto
    location: strawberry.auto
    start_date: strawberry.auto
    end_date: strawberry.auto


@strawberry_django.input(EventAsset)
class CreateEventAssetsInput:
    event: strawberry.ID
    image: Upload


@strawberry_django.input(Report)
class CreateReportInput:
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    report_file: Upload


@strawberry_django.partial(Report)
class UpdateReportInput:
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    status: strawberry.auto
    report_file: Upload | None = strawberry.UNSET


@strawberry_django.input(GalleryItem)
class GalleryItemInput:
    image: Upload
    image_type: ImageTypeEnum


@strawberry_django.partial(GalleryItem)
class DeleteGalleryItemInput:
    id: strawberry.auto


@strawberry_django.input(YouTubeVideo)
class YoutubeVideoInput:
    title: strawberry.auto
    video_url: strawberry.auto
    release_date: strawberry.auto
    thumbnail: Upload


@strawberry_django.partial(YouTubeVideo)
class UpdateYoutubeVideoInput:
    title: strawberry.auto
    video_url: strawberry.auto
    release_date: strawberry.auto
    thumbnail: Upload | None = strawberry.UNSET
