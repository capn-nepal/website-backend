import strawberry
import strawberry_django

from apps.team.models import TeamMember, TeamMemberTypeEnum


@strawberry_django.filters.filter(TeamMember, lookups=True)
class TeamMemberFilter:
    id: strawberry.auto
    member_type: TeamMemberTypeEnum | None
