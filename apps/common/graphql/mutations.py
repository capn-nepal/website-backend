import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from strawberry_django.mutations import delete
from strawberry_django.permissions import IsAuthenticated

from apps.common.graphql.inputs import (
    CreateEventAssetsInput,
    CreateEventInput,
    CreateReportInput,
    DeleteGalleryItemInput,
    GalleryItemInput,
    UpdateEventInput,
    UpdateReportInput,
    UpdateYoutubeVideoInput,
    YoutubeVideoInput,
)
from apps.common.graphql.types import EventAssetType, EventType, GalleryItemType, ReportType, YouTubeVideoType
from apps.common.models import Event, Report, YouTubeVideo
from apps.common.serializers import (
    CreateReportSerializer,
    EventAssetsSerializer,
    EventSerializer,
    GalleryItemSerializer,
    UpdateReportSerializer,
    YoutubeVideoSerializer,
)
from main.graphql.context import Info
from utils.graphql.mutations import ModelMutation
from utils.graphql.types import MutationResponseType


@strawberry.type
class Mutation:
    # Event --------------------------
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_event(self, info: Info, data: CreateEventInput) -> MutationResponseType[EventType]:
        return await ModelMutation(EventSerializer).handle_create_mutation(data, info, None)

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
        return await ModelMutation(EventSerializer).handle_update_mutation(data, info, event)

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

    # Images -----------------------------------
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def add_gallery_item(self, info: Info, data: GalleryItemInput) -> MutationResponseType[GalleryItemType]:
        return await ModelMutation(GalleryItemSerializer).handle_create_mutation(data, info, None)

    delete_gallery_item: GalleryItemType = delete(
        DeleteGalleryItemInput,
        key_attr="id",
        extensions=[IsAuthenticated()],
    )

    # youtube videos -----------------------------------
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def add_youtube_video(self, info: Info, data: YoutubeVideoInput) -> MutationResponseType[YouTubeVideoType]:
        return await ModelMutation(YoutubeVideoSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_youtube_video(
        self,
        info: Info,
        data: UpdateYoutubeVideoInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[YouTubeVideoType]:
        video = await YouTubeVideo.objects.aget(pk=pk)
        return await ModelMutation(YoutubeVideoSerializer).handle_update_mutation(data, info, video)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def archive_youtube_video(
        self,
        info: Info,
        pk: strawberry.ID,
    ) -> MutationResponseType[YouTubeVideoType]:
        video = await YouTubeVideo.objects.aget(pk=pk)
        if video.is_archived:
            return MutationResponseType(ok=False, errors=["Video is already archived."])  # type: ignore[reportReturnType]
        video.is_archived = True
        await sync_to_async(video.save)(update_fields=["is_archived"])
        return MutationResponseType(ok=True, errors=None)  # type: ignore[reportReturnType]
