import strawberry
import strawberry_django
from strawberry.file_uploads import Upload

from apps.blog.models import Author, Blog, BlogAsset


@strawberry_django.input(Blog)
class CreateBlogInput:
    title: strawberry.auto
    published_date: strawberry.auto
    description: strawberry.auto
    featured: strawberry.auto
    content: strawberry.auto
    author: strawberry.ID
    cover_image: Upload


@strawberry_django.partial(Blog)
class UpdateBlogInput:
    title: strawberry.auto
    published_date: strawberry.auto
    author: strawberry.auto
    description: strawberry.auto
    featured: strawberry.auto
    content: strawberry.auto
    status: strawberry.auto
    cover_image: Upload | None = strawberry.UNSET


@strawberry_django.input(BlogAsset)
class CreateBlogAssetsInput:
    blog: strawberry.ID
    file: Upload


@strawberry_django.input(Author)
class AddAuthorInput:
    name: strawberry.auto
    image: Upload | None = strawberry.UNSET


@strawberry_django.partial(Author)
class UpdateAuthorInput:
    name: strawberry.auto
    image: Upload | None = strawberry.UNSET
