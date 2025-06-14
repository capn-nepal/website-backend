import strawberry
import strawberry_django

from apps.vacancy.models import EmploymentTypeEnum, JobVacancy, Position


@strawberry_django.filters.filter(JobVacancy, lookups=True)
class JobVacancyFilter:
    deadline: strawberry.auto
    is_archived: bool | None = strawberry.UNSET


@strawberry_django.filters.filter(Position, lookups=True)
class PositionFilter:
    employment_type: EmploymentTypeEnum | None = strawberry.UNSET
    is_archived: bool | None = strawberry.UNSET
