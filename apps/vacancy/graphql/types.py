import strawberry
import strawberry_django
from asgiref.sync import sync_to_async

from apps.vacancy.models import EmploymentTypeEnum, JobVacancy, Position


@strawberry_django.type(Position)
class PositionType:
    id: strawberry.ID
    name: strawberry.auto
    summary: strawberry.auto
    description: strawberry.auto

    @strawberry.field
    @sync_to_async
    def employment_type(self) -> str:
        return EmploymentTypeEnum(self.employment_type).label


@strawberry_django.type(JobVacancy)
class JobVacancyType:
    id: strawberry.ID
    description: strawberry.auto
    position: PositionType
    number_of_vacancies: strawberry.auto
    deadline: strawberry.auto
