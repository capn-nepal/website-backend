import strawberry_django
from datetime import date

from apps.blog.models import Blog


@strawberry_django.type(Blog)
class BlogType:
    id: int
    title: str
    published_date: date
    author: str
    description: str
    cover_image: str
    featured: bool
