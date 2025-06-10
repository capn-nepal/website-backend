import strawberry
import strawberry_django

from apps.vacancy.models import JobVacancy, Position


@strawberry_django.type(JobVacancy)
class JobVacancyType:
    id: strawberry.ID
    description: strawberry.auto
    position: strawberry.auto
    number_of_vacancies: strawberry.auto
    deadline: strawberry.auto


@strawberry_django.type(Position)
class PositionType:
    id: strawberry.ID
    name: strawberry.auto
    summary: strawberry.auto
    description: strawberry.auto
    employment_type: strawberry.auto
