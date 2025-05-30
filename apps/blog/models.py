from django.db import models
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from apps.common.models import UserResource


class BlogStatusEnum(models.IntegerChoices):
    DRAFT = 50, "Draft"
    PUBLISHED = 60, "Published"
    ARCHIVED = 70, "Archived"


class Author(UserResource):
    name = models.CharField(max_length=200, verbose_name=("Name"))
    image = models.ImageField(verbose_name=_("Author Image"), upload_to="author/", null=True, blank=True)

    def __str__(self):
        return self.name


class Blog(UserResource):
    title = models.CharField(max_length=232, verbose_name=_("Title"))
    published_date = models.DateField(verbose_name=_("Published Date"))
    author = models.ForeignKey(
        Author,
        related_name="blogs",
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
    )
    content = models.TextField(verbose_name=_("Content"))
    description = models.CharField(verbose_name=_("Description"))
    cover_image = models.ImageField(
        upload_to="blogs/",
        verbose_name=_("Cover Image"),
    )
    featured = models.BooleanField(verbose_name=_("Featured"), default=False)
    status: int = IntegerChoicesField(choices_enum=BlogStatusEnum, default=BlogStatusEnum.DRAFT)  # type: ignore[reportAssignmentType]

    def __str__(self):
        return self.title


class BlogAsset(UserResource):
    file = models.FileField(verbose_name=_("File"))
    blog = models.ForeignKey(
        Blog,
        related_name="%(class)s_file",
        on_delete=models.PROTECT,
    )
