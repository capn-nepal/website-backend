import strawberry
import strawberry_django
from strawberry.file_uploads import Upload

from apps.news.models import News, NewsTypeEnum, StatusEnum


@strawberry_django.input(News)
class CreateNewsInput:
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    news_type: NewsTypeEnum
    cover_image: Upload | None = strawberry.UNSET


@strawberry_django.partial(News)
class UpdateNewsInput:
    title: strawberry.auto
    description: strawberry.auto
    published_date: strawberry.auto
    news_type: NewsTypeEnum | None = strawberry.UNSET
    status: StatusEnum | None = strawberry.UNSET
    cover_image: Upload | None = strawberry.UNSET
