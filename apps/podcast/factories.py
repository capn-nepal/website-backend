import factory
from django.core.files.base import ContentFile
from factory.django import DjangoModelFactory

from apps.podcast.models import PodcastEpisode, PodcastSeason, VoxPop, VoxPopEpisode
from apps.user.factories import UserFactory


class PodcastSeasonFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = PodcastSeason


class PodcastEpisodeFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    podcast_season = factory.SubFactory(PodcastSeasonFactory)
    thumbnail = factory.LazyFunction(lambda: ContentFile(b"fake_image_data", name="fake_image.jpg"))

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = PodcastEpisode


class VoxPopFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = VoxPop


class VoxPopEpisodeFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    voxpop_season = factory.SubFactory(VoxPopFactory)
    thumbnail = factory.LazyFunction(lambda: ContentFile(b"fake_image_data2", name="fake_image2.jpg"))

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = VoxPopEpisode
