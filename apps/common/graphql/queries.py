import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsAuthenticated

from .filters import EventFilter, ReportFilter
from .orders import EventOrder, ReportOrder
from .types import EventAssetType, EventType, ReportType


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
