from django.db import models
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from apps.common.models import StatusEnum, UserResource


class NewsTypeEnum(models.IntegerChoices):
    NEWS = 100, "News"
    OTHER_UPDATE = 200, "Other Update"


class News(UserResource):
    title = models.CharField(max_length=250, verbose_name=_("News Title"))
    description = models.TextField(verbose_name=_("News Description"))
    published_date = models.DateTimeField(verbose_name=_("News Published Date"))
    status: int = IntegerChoicesField(choices_enum=StatusEnum, default=StatusEnum.DRAFT)  # type: ignore[reportAssignmentType]
    news_type: int = IntegerChoicesField(choices_enum=NewsTypeEnum, default=NewsTypeEnum.NEWS)  # type: ignore[reportAssignmentType]

    def __str__(self):
        return self.title
