import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from strawberry_django.permissions import IsAuthenticated

from apps.common.graphql.inputs import (
    CreateEventAssetsInput,
    CreateEventInput,
    CreateReportInput,
    UpdateEventInput,
    UpdateReportInput,
)
from apps.common.graphql.types import EventAssetType, EventType, ReportType
from apps.common.models import Event, Report
from apps.common.serializers import (
    CreateEventSerializer,
    CreateReportSerializer,
    EventAssetsSerializer,
    UpdateEventSerializer,
    UpdateReportSerializer,
)
from main.graphql.context import Info
from utils.graphql.mutations import ModelMutation
from utils.graphql.types import MutationResponseType


@strawberry.type
class Mutation:
    # Event --------------------------
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_event(self, info: Info, data: CreateEventInput) -> MutationResponseType[EventType]:
        return await ModelMutation(CreateEventSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_event_asset(self, info: Info, data: CreateEventAssetsInput) -> MutationResponseType[EventAssetType]:
        return await ModelMutation(EventAssetsSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_event(
        self,
        info: Info,
        data: UpdateEventInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[EventType]:
        event = await Event.objects.aget(pk=pk)
        return await ModelMutation(UpdateEventSerializer).handle_update_mutation(data, info, event)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def archive_event(
        self,
        info: Info,
        pk: strawberry.ID,
    ) -> MutationResponseType[EventType]:
        event = await Event.objects.aget(pk=pk)
        if event.is_deleted:
            return MutationResponseType(ok=False, errors=["Event is already archived."])  # type: ignore[reportReturnType]
        event.is_deleted = True
        await sync_to_async(event.save)(update_fields=["is_deleted"])
        return MutationResponseType(ok=True, errors=None)  # type: ignore[reportReturnType]

    # Report -----------------------------------------------------
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_report(self, info: Info, data: CreateReportInput) -> MutationResponseType[ReportType]:
        return await ModelMutation(CreateReportSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_report(
        self,
        info: Info,
        data: UpdateReportInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[ReportType]:
        report = await Report.objects.aget(pk=pk)
        return await ModelMutation(UpdateReportSerializer).handle_update_mutation(data, info, report)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def archive_report(
        self,
        info: Info,
        pk: strawberry.ID,
    ) -> MutationResponseType[ReportType]:
        report = await Report.objects.aget(pk=pk)
        if report.is_deleted:
            return MutationResponseType(ok=False, errors=["Report is already archived."])  # type: ignore[reportReturnType]
        report.is_deleted = True
        await sync_to_async(report.save)(update_fields=["is_deleted"])
        return MutationResponseType(ok=True, errors=None)  # type: ignore[reportReturnType]
