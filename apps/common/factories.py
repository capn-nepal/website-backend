import factory
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from factory.django import DjangoModelFactory

from apps.common.models import (
    Artwork,
    Event,
    Gallery,
    GalleryItem,
    Report,
    YouTubeVideo,
)
from apps.user.factories import UserFactory


class EventFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = Event


class EventAssetsFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    event = factory.SubFactory(Event)
    image = factory.LazyFunction(lambda: ContentFile(b"fake_image_data", name="fake_image.jpg"))


class ReportFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    report_file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            "report.csv",
            b"id,name\n1,Test Report\n2,Another Report",
            content_type="text/csv",
        ),
    )

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = Report


class YouTubeVideoFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    thumbnail = factory.LazyFunction(lambda: ContentFile(b"fake_image_data", name="thumbnail_image.jpg"))

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = YouTubeVideo


class GalleryFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = Gallery


class GalleryItemFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    gallery = factory.SubFactory(GalleryFactory)
    image = factory.LazyFunction(lambda: ContentFile(b"fake_image_data", name="fake_gallery_image.jpg"))

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = GalleryItem


class ArtworkFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    image = factory.LazyFunction(lambda: ContentFile(b"fake_image_data", name="fake_artwork_image.jpg"))

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = Artwork
