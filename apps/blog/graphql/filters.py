import strawberry
import strawberry_django

from apps.blog.models import Blog, BlogAsset, BlogStatusEnum


@strawberry_django.filters.filter(Blog, lookups=True)
class BlogFilter:
    id: strawberry.auto
    title: strawberry.auto
    status: BlogStatusEnum


@strawberry_django.filters.filter(BlogAsset, lookups=True)
class BlogAssetsFilter:
    id: strawberry.auto
