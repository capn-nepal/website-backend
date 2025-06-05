import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from strawberry_django.permissions import IsAuthenticated

from apps.vacancy.graphql.inputs import (
    CreateJobVacancyInput,
    CreatePositionInput,
    UpdateJobVacancyInput,
    UpdatePositionInput,
)
from apps.vacancy.graphql.types import JobVacancyType, PositionType
from apps.vacancy.models import JobVacancy, Position
from apps.vacancy.serializers import (
    CreateJobVacancySerializer,
    CreatePositionSerializer,
    UpdateJobVacancySerializer,
    UpdatePositionSerializer,
)
from main.graphql.context import Info
from utils.graphql.mutations import ModelMutation
from utils.graphql.types import MutationResponseType


@strawberry.type
class Mutation:
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_job_vacancy(self, info: Info, data: CreateJobVacancyInput) -> MutationResponseType[JobVacancyType]:
        return await ModelMutation(CreateJobVacancySerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_job_vacancy(
        self,
        info: Info,
        data: UpdateJobVacancyInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[JobVacancyType]:
        job_vacancy = await JobVacancy.objects.aget(pk=pk)
        return await ModelMutation(UpdateJobVacancySerializer).handle_update_mutation(data, info, job_vacancy)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def archive_job_vacancy(
        self,
        info: Info,
        pk: strawberry.ID,
    ) -> MutationResponseType[JobVacancyType]:
        job_vacancy = await JobVacancy.objects.aget(pk=pk)
        if job_vacancy.is_archived:
            return MutationResponseType(ok=False, errors=["This Vacancy is already archived."])  # type: ignore[reportReturnType]
        job_vacancy.is_archived = True
        await sync_to_async(job_vacancy.save)(update_fields=["is_archived"])
        return MutationResponseType(ok=True, errors=None)  # type: ignore[reportReturnType]

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_position(self, info: Info, data: CreatePositionInput) -> MutationResponseType[PositionType]:
        return await ModelMutation(CreatePositionSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_position(
        self,
        info: Info,
        data: UpdatePositionInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[PositionType]:
        position = await Position.objects.aget(pk=pk)
        return await ModelMutation(UpdatePositionSerializer).handle_update_mutation(data, info, position)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def archive_posotion(
        self,
        info: Info,
        pk: strawberry.ID,
    ) -> MutationResponseType[PositionType]:
        position = await Position.objects.aget(pk=pk)
        if position.is_archived:
            return MutationResponseType(ok=False, errors=["This Position is already archived."])  # type: ignore[reportReturnType]
        position.is_archived = True
        await sync_to_async(position.save)(update_fields=["is_archived"])
        return MutationResponseType(ok=True, errors=None)  # type: ignore[reportReturnType]
