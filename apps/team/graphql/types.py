import strawberry
import strawberry_django
from asgiref.sync import sync_to_async

from apps.team.models import TeamMember, TeamMemberTypeEnum


@strawberry_django.type(TeamMember)
class TeamMemberType:
    id: strawberry.ID
    first_name: strawberry.auto
    middle_name: strawberry.auto
    last_name: strawberry.auto
    designation: strawberry.auto
    member_photo: strawberry.auto
    bio: strawberry.auto

    @strawberry.field
    @sync_to_async
    def member_type(self) -> str:
        return TeamMemberTypeEnum(self.member_type).label
