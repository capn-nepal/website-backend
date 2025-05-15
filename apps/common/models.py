from django.db import models
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from apps.user.models import User


# -- Abstracts
class UserResource(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name="%(class)s_created",
        on_delete=models.PROTECT,
    )
    modified_by = models.ForeignKey(
        User,
        related_name="%(class)s_modified",
        on_delete=models.PROTECT,
    )

    # Typing
    id: int
    pk: int
    created_by_id: int
    modified_by_id: int

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        abstract = True
        ordering = ["-id"]


class StatusEnum(models.IntegerChoices):
    DRAFT = 101, "Draft"
    PUBLISHED = 102, "Published"


class Event(UserResource):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    description = models.TextField(max_length=200, verbose_name=_("Description"))
    location = models.CharField(verbose_name=_("Location"), null=True, blank=True)
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class EventAsset(UserResource):  # noqa: DJ008
    event = models.ForeignKey(
        Event,
        related_name="%(class)s_file",
        on_delete=models.PROTECT,
    )
    image = models.ImageField(verbose_name=_("Event Images"))


class Report(UserResource):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    published_date = models.DateField(verbose_name=_("Published Date"))
    report_file = models.FileField(upload_to="reports/", verbose_name=_("Report File"))
    is_deleted = models.BooleanField(default=False)
    status: int = IntegerChoicesField(choices_enum=StatusEnum, null=True, blank=True)  # type: ignore[reportAssignmentType]

    def __str__(self):
        return self.title
