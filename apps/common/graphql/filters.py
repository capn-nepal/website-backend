import strawberry
import strawberry_django

from apps.common.models import Event, Report, StatusEnum


@strawberry_django.filters.filter(Event, lookups=True)
class EventFilter:
    id: strawberry.auto
    is_deleted: bool


@strawberry_django.filters.filter(Report, lookups=True)
class ReportFilter:
    id: strawberry.auto
    status: StatusEnum
    is_deleted: bool
