import factory
from factory.django import DjangoModelFactory

from apps.user.factories import UserFactory
from apps.vacancy.models import JobVacancy, Position


class PositionFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = Position


class JobVacancyFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    position = factory.SubFactory(PositionFactory)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = JobVacancy
