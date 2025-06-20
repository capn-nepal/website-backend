import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated

from .filters import NewsFilter
from .orders import NewsOrder
from .types import NewsType


@strawberry.type
class Query:
    news: OffsetPaginated[NewsType] = strawberry_django.offset_paginated(
        order=NewsOrder,
        filters=NewsFilter,
        extensions=[],
    )
