import factory
from django.core.files.base import ContentFile
from factory.django import DjangoModelFactory

from apps.team.models import TeamMember
from apps.user.factories import UserFactory


class TeamMemberFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    member_photo = factory.LazyFunction(lambda: ContentFile(b"fake_image_data", name="member_image.jpg"))

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = TeamMember
