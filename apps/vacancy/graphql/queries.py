import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsAuthenticated

from .filters import JobVacancyFilter, PositionFilter
from .orders import JobVacancyOrder, PositionOrder
from .types import JobVacancyType, PositionType


@strawberry.type
class Query:
    job_vacancies: OffsetPaginated[JobVacancyType] = strawberry_django.offset_paginated(
        order=JobVacancyOrder,
        filters=JobVacancyFilter,
        extensions=[IsAuthenticated()],
    )
    job_vacancy: JobVacancyType = strawberry_django.field(extensions=[IsAuthenticated()])

    positions: OffsetPaginated[PositionType] = strawberry_django.offset_paginated(
        order=PositionOrder,
        filters=PositionFilter,
        extensions=[IsAuthenticated()],
    )

    position: PositionType = strawberry_django.field(extensions=[IsAuthenticated()])
