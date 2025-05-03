from django.db import models
from apps.common.models import UserResource
from django.utils.translation import gettext_lazy as _


class Blog(UserResource):
    title = models.CharField(max_length=232, verbose_name=_('Title'))
    published_date = models.DateField(verbose_name=_('Published Date'))
    author = models.CharField(max_length=232, verbose_name=_('Author'))
    content = models.TextField(verbose_name=_('Content'))
    description = models.CharField(verbose_name=_('Description'))
    cover_image = models.ImageField(
        upload_to='blogs/',
        verbose_name=_('Cover Image')
    )
    featured = models.BooleanField(verbose_name=_('Featured'), default=False)

    def __str__(self):
        return self.title


class BlogAsset(UserResource):
    file = models.FileField(verbose_name=_('File'))
    blog = models.ForeignKey(
        Blog,
        related_name="%(class)s_file",
        on_delete=models.PROTECT,
    )
