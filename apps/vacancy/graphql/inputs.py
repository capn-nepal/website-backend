import strawberry
import strawberry_django

from apps.vacancy.models import EmploymentTypeEnum, JobVacancy, Position


@strawberry_django.input(JobVacancy)
class CreateJobVacancyInput:
    position: strawberry.ID
    description: strawberry.auto
    number_of_vacancies: strawberry.auto
    deadline: strawberry.auto


@strawberry_django.partial(JobVacancy)
class UpdateJobVacancyInput:
    description: strawberry.auto
    number_of_vacancies: strawberry.auto
    deadline: strawberry.auto
    position: strawberry.ID | None = strawberry.UNSET


@strawberry_django.input(Position)
class CreatePositionInput:
    name: strawberry.auto
    summary: strawberry.auto
    description: strawberry.auto
    employment_type: EmploymentTypeEnum


@strawberry_django.partial(Position)
class UpdatePositionInput:
    name: strawberry.auto
    summary: strawberry.auto
    description: strawberry.auto
    employment_type: strawberry.auto
