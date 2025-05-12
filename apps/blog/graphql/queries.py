import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated

from .filters import BlogAssetsFilter, BlogFilter
from .orders import BlogAssetsOrder, BlogOrder
from .types import BlogAssetsType, BlogType


@strawberry.type
class Query:
    # Public --------------------
    # --- Paginated
    blogs: OffsetPaginated[BlogType] = strawberry_django.offset_paginated(
        order=BlogOrder,
        filters=BlogFilter,
    )
    blog: BlogType = strawberry_django.field(extensions=[])

    # blog assets
    blog_assets: OffsetPaginated[BlogAssetsType] = strawberry_django.offset_paginated(
        order=BlogAssetsOrder,
        filters=BlogAssetsFilter,
    )

    blog_asset: BlogAssetsType = strawberry_django.field(extensions=[])
