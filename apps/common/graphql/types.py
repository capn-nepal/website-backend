import datetime

import strawberry
import strawberry_django

from apps.common.models import Event, EventAsset, GalleryImage, Report
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
    event: strawberry.auto
    image: strawberry.auto


@strawberry_django.type(Report)
class ReportType:
    id: strawberry.ID
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    report_file: strawberry.auto
    is_deleted: strawberry.auto
    status: strawberry.auto


@strawberry_django.type(GalleryImage)
class ImageType:
    id: strawberry.auto
    image: strawberry.auto
