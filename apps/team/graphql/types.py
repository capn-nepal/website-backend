import strawberry
import strawberry_django

from apps.team.models import TeamMember


@strawberry_django.type(TeamMember)
class TeamMemberType:
    id: strawberry.ID
    first_name: strawberry.auto
    middle_name: strawberry.auto
    last_name: strawberry.auto
    designation: strawberry.auto
    member_photo: strawberry.auto
    member_type: strawberry.auto
