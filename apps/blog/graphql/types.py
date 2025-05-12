import strawberry
import strawberry_django

from apps.blog.models import Blog, BlogAsset


@strawberry_django.type(Blog)
class BlogType:
    id: strawberry.ID
    title: strawberry.auto
    published_date: strawberry.auto
    author: strawberry.auto
    description: strawberry.auto
    cover_image: strawberry.auto
    featured: strawberry.auto
    content: strawberry.auto


@strawberry_django.type(BlogAsset)
class BlogAssetsType:
    id: strawberry.ID
    blog: strawberry.auto
    file: strawberry.auto
