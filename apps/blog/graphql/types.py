import strawberry
import strawberry_django

from apps.blog.models import Author, Blog, BlogAsset


@strawberry_django.type(Author)
class AuthorType:
    id: strawberry.ID
    name: strawberry.auto
    image: strawberry.auto


@strawberry_django.type(Blog)
class BlogType:
    id: strawberry.ID
    title: strawberry.auto
    published_date: strawberry.auto
    author: AuthorType
    description: strawberry.auto
    cover_image: strawberry.auto
    featured: strawberry.auto
    content: strawberry.auto
    status: strawberry.auto


@strawberry_django.type(BlogAsset)
class BlogAssetsType:
    id: strawberry.ID
    blog: BlogType
    file: strawberry.auto
