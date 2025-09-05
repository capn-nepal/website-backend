from django.db import models
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from apps.user.models import User
from utils.fields import SecureFileField, SecureImageField


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
    DRAFT = 50, "Draft"
    PUBLISHED = 60, "Published"
    ARCHIVED = 70, "Archived"


class Event(UserResource):
    name = models.CharField(max_length=200, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("Description"))
    location = models.CharField(verbose_name=_("Location"), null=True, blank=True)
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    is_deleted = models.BooleanField(default=False)
    thumbnail = SecureImageField(upload_to="event-thumbnails/", blank=True, null=True)

    def __str__(self):
        return self.name


class EventAsset(UserResource):  # noqa: DJ008
    event = models.ForeignKey(
        Event,
        related_name="%(class)s_file",
        on_delete=models.PROTECT,
    )
    image = SecureImageField(verbose_name=_("Event Images"))


class Report(UserResource):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    published_date = models.DateField(verbose_name=_("Published Date"))
    report_file = SecureFileField(upload_to="reports/", verbose_name=_("Report File"))
    cover_image = SecureImageField(upload_to="report_cover_image/", verbose_name=_("Report File"))
    status: int = IntegerChoicesField(choices_enum=StatusEnum, default=StatusEnum.DRAFT)  # type: ignore[reportAssignmentType]

    def __str__(self):
        return self.title


class Gallery(UserResource):
    name = models.CharField(max_length=255, verbose_name=_("Gallery Name"))
    description = models.TextField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GalleryItem(UserResource):
    gallery = models.ForeignKey(Gallery, related_name="gallery_images", on_delete=models.PROTECT)
    image = SecureImageField(upload_to="gallery_images/")
    caption = models.CharField(max_length=255, blank=True, verbose_name=_("Image Caption"))
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Image in {self.gallery.name}"


class Artwork(UserResource):
    name = models.CharField(max_length=200, verbose_name=_("Art Work Name"))
    image = SecureImageField(upload_to="artwork_images/")

    def __str__(self):
        return self.name


class YouTubeVideo(UserResource):
    title = models.CharField(max_length=255, verbose_name=_("Video Title"))
    video_url = models.URLField(verbose_name=_("Youtube Video Url"))
    thumbnail = SecureImageField(upload_to="thumbnails/", blank=True, null=True)
    release_date = models.DateTimeField(verbose_name=_(" Video Release Date"))
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Changemaker(UserResource):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    logo = SecureImageField(upload_to="changemakers/", blank=True, null=True, verbose_name=_("Logo"))
    description = models.TextField(verbose_name=_("Description"))
    facebook_link = models.URLField(blank=True, null=True, verbose_name=_("Facebook Link"))
    linkdin_link = models.URLField(blank=True, null=True, verbose_name=_("Linkdin Link"))
    instagram_link = models.URLField(blank=True, null=True, verbose_name=_("Instagram Link"))
    website_link = models.URLField(blank=True, null=True, verbose_name=_("Website Link"))
    is_archived = models.BooleanField(default=False)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        verbose_name = _("Community of changemaker")
        verbose_name_plural = _("Community of changemakers")

    def __str__(self):
        return self.name
