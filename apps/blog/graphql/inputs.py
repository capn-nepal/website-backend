import strawberry
import strawberry_django
from strawberry.file_uploads import Upload

from apps.blog.models import Blog, BlogAsset


@strawberry_django.input(Blog)
class CreateBlogInput:
    title: strawberry.auto
    published_date: strawberry.auto
    description: strawberry.auto
    cover_image: strawberry.auto
    featured: strawberry.auto
    content: strawberry.auto


@strawberry_django.partial(Blog)
class UpdateBlogInput:
    title: strawberry.auto
    published_date: strawberry.auto
    author: strawberry.auto
    description: strawberry.auto
    featured: strawberry.auto
    content: strawberry.auto
    cover_image: strawberry.ID | None = strawberry.UNSET


@strawberry_django.input(BlogAsset)
class CreateBlogAssetsInput:
    blog: strawberry.ID
    file: Upload
