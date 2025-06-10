import strawberry
import strawberry_django

from apps.news.models import News


@strawberry_django.type(News)
class NewsType:
    id: strawberry.ID
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    status: strawberry.auto
    news_type: strawberry.auto
