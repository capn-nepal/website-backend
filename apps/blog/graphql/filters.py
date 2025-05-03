import strawberry
import strawberry_django

from apps.blog.models import Blog


@strawberry_django.filters.filter(Blog, lookups=True)
class BlogFilter:
    id: strawberry.auto
    title: strawberry.auto
