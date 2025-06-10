import strawberry
import strawberry_django

from apps.team.models import TeamMember


@strawberry_django.ordering.order(TeamMember)
class TeamMemberOrder:
    id: strawberry.auto
