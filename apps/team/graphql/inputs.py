import strawberry
import strawberry_django
from strawberry.file_uploads import Upload

from apps.team.models import TeamMember


@strawberry_django.input(TeamMember)
class CreateTeamMemberInput:
    first_name: strawberry.auto
    middle_name: strawberry.auto
    last_name: strawberry.auto
    designation: strawberry.auto
    member_photo: Upload
    member_type: strawberry.auto
    bio: strawberry.auto
    linkedin_link: strawberry.auto
    instagram_link: strawberry.auto
    facebook_link: strawberry.auto
    member_order: strawberry.auto


@strawberry_django.partial(TeamMember)
class UpdateTeamMemberInput:
    first_name: strawberry.auto
    middle_name: strawberry.auto
    last_name: strawberry.auto
    designation: strawberry.auto
    member_type: strawberry.auto
    bio: strawberry.auto
    linkedin_link: strawberry.auto
    instagram_link: strawberry.auto
    facebook_link: strawberry.auto
    member_order: strawberry.auto
    member_photo: Upload | None = strawberry.UNSET


@strawberry_django.input(TeamMember)
class DeleteTeamMemberInput:
    id: strawberry.auto
