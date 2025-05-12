import strawberry
import strawberry_django

from apps.blog.models import Blog, BlogAsset


@strawberry_django.ordering.order(Blog)
class BlogOrder:
    id: strawberry.auto
    title: strawberry.auto


@strawberry_django.ordering.order(BlogAsset)
class BlogAssetsOrder:
    id: strawberry.auto
