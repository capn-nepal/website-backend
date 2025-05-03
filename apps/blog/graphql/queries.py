import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated

from .filters import BlogFilter
from .orders import BlogOrder
from .types import BlogType


@strawberry.type
class Query:
    # Public --------------------
    # --- Paginated
    blogs: OffsetPaginated[BlogType] = strawberry_django.offset_paginated(
        order=BlogOrder,
        filters=BlogFilter,
        extensions=[],
    )
