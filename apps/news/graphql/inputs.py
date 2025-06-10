import strawberry
import strawberry_django

from apps.news.models import News, NewsTypeEnum, StatusEnum


@strawberry_django.input(News)
class CreateNewsInput:
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    news_type: NewsTypeEnum


@strawberry_django.partial(News)
class UpdateNewsInput:
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    news_type: NewsTypeEnum | None = strawberry.UNSET
    status: StatusEnum | None = strawberry.UNSET
