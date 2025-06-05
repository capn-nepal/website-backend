import strawberry
import strawberry_django

from apps.vacancy.models import EmployMentTypeEnum, JobVacancy, Position


@strawberry_django.filters.filter(JobVacancy, lookups=True)
class JobVacancyFilter:
    id: strawberry.auto
    deadline: strawberry.auto
    is_archived: bool | None


@strawberry_django.filters.filter(Position, lookups=True)
class PositionFilter:
    id: strawberry.auto
    employment_type: EmployMentTypeEnum | None
    is_archived: bool | None
