import strawberry
import strawberry_django

from apps.common.models import StatusEnum
from apps.news.models import News, NewsTypeEnum


@strawberry_django.filters.filter(News, lookups=True)
class NewsFilter:
    id: strawberry.auto
    news_type: NewsTypeEnum | None
    status: StatusEnum | None
