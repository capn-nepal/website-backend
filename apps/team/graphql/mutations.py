import strawberry
import strawberry_django
from strawberry_django.mutations import delete
from strawberry_django.permissions import IsAuthenticated

from apps.team.models import TeamMember
from apps.team.serializers import CreateTeamMemberSerializer, UpdateTeamMemberSerializer
from main.graphql.context import Info
from utils.graphql.mutations import ModelMutation
from utils.graphql.types import MutationResponseType

from .inputs import CreateTeamMemberInput, DeleteTeamMemberInput, UpdateTeamMemberInput
from .types import TeamMemberType


@strawberry.type
class Mutation:
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def add_team_member(self, info: Info, data: CreateTeamMemberInput) -> MutationResponseType[TeamMemberType]:
        return await ModelMutation(CreateTeamMemberSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_team_member(
        self,
        info: Info,
        data: UpdateTeamMemberInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[TeamMemberType]:
        report = await TeamMember.objects.aget(pk=pk)
        return await ModelMutation(UpdateTeamMemberSerializer).handle_update_mutation(data, info, report)

    delete_team_member: TeamMemberType = delete(
        DeleteTeamMemberInput,
        key_attr="id",
        extensions=[IsAuthenticated()],
    )
