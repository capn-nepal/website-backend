from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from apps.common.models import StatusEnum, UserResource
from utils.common import unique_slugify


class NewsTypeEnum(models.IntegerChoices):
    NEWS = 100, "News"
    OTHER_UPDATE = 200, "Other Update"


class News(UserResource):
    title = models.CharField(max_length=250, verbose_name=_("News Title"))
    description = models.TextField(verbose_name=_("News Description"))
    published_date = models.DateTimeField(verbose_name=_("News Published Date"))
    status: int = IntegerChoicesField(choices_enum=StatusEnum, default=StatusEnum.DRAFT)  # type: ignore[reportAssignmentType]
    news_type: int = IntegerChoicesField(choices_enum=NewsTypeEnum, default=NewsTypeEnum.NEWS)  # type: ignore[reportAssignmentType]
    slug = models.SlugField(unique=True, max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)
