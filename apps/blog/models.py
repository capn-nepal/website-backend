from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from apps.common.models import StatusEnum, UserResource
from utils.common import unique_slugify
from utils.fields import SecureFileField, SecureImageField


class Author(UserResource):
    name = models.CharField(max_length=200, verbose_name=("Name"))
    image = SecureImageField(verbose_name=_("Author Image"), upload_to="author/", null=True, blank=True)

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
    cover_image = SecureImageField(
        upload_to="blogs/",
        verbose_name=_("Cover Image"),
    )
    featured = models.BooleanField(verbose_name=_("Featured"), default=False)
    status: int = IntegerChoicesField(choices_enum=StatusEnum, default=StatusEnum.DRAFT)  # type: ignore[reportAssignmentType]
    slug = models.SlugField(unique=True, max_length=250, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogAsset(UserResource):
    file = SecureFileField(verbose_name=_("File"))
    blog = models.ForeignKey(
        Blog,
        related_name="%(class)s_file",
        on_delete=models.PROTECT,
    )
