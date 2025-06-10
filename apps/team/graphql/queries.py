import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsAuthenticated

from .filters import TeamMemberFilter
from .orders import TeamMemberOrder
from .types import TeamMemberType


@strawberry.type
class Query:
    team_members: OffsetPaginated[TeamMemberType] = strawberry_django.offset_paginated(
        order=TeamMemberOrder,
        filters=TeamMemberFilter,
        extensions=[IsAuthenticated()],
    )
    team_member: TeamMemberType = strawberry_django.field(extensions=[IsAuthenticated()])
