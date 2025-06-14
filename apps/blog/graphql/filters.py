import strawberry
import strawberry_django

from apps.blog.models import Blog, BlogAsset
from apps.common.models import StatusEnum


@strawberry_django.filters.filter(Blog, lookups=True)
class BlogFilter:
    id: strawberry.auto
    title: strawberry.auto
    status: StatusEnum | None = strawberry.UNSET


@strawberry_django.filters.filter(BlogAsset, lookups=True)
class BlogAssetsFilter:
    id: strawberry.auto
