import strawberry
import strawberry_django
from asgiref.sync import sync_to_async

from apps.news.models import News, NewsTypeEnum


@strawberry_django.type(News)
class NewsType:
    id: strawberry.ID
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    status: strawberry.auto
    slug: strawberry.auto

    @strawberry.field
    @sync_to_async
    def news_type(self) -> str:
        return NewsTypeEnum(self.news_type).label
