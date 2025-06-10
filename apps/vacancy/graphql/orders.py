import strawberry
import strawberry_django

from apps.vacancy.models import JobVacancy, Position


@strawberry_django.ordering.order(JobVacancy)
class JobVacancyOrder:
    id: strawberry.auto


@strawberry_django.ordering.order(Position)
class PositionOrder:
    id: strawberry.auto
    name: strawberry.auto
