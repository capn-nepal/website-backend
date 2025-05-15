import strawberry
import strawberry_django

from apps.common.models import Event, Report


@strawberry_django.ordering.order(Event)
class EventOrder:
    id: strawberry.auto


@strawberry_django.ordering.order(Report)
class ReportOrder:
    id: strawberry.auto
