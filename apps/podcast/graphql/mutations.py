import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from strawberry_django.permissions import IsAuthenticated

from apps.podcast.graphql.inputs import (
    CreatePodcastEpisodeInput,
    CreatePodcastSeasonInput,
    CreateVoxPopEpisodeInput,
    CreateVoxPopInput,
    UpdatePodcastEpisodeInput,
    UpdatePodcastSeasonInput,
    UpdateVoxPopEpisodeInput,
    UpdateVoxPopInput,
)
from apps.podcast.graphql.types import (
    PodcastEpisodeType,
    PodcastSeasonType,
    VoxPopEpisodeType,
    VoxPopSeasonType,
)
from apps.podcast.models import PodcastEpisode, PodcastSeason, VoxPop, VoxPopEpisode
from apps.podcast.serializers import (
    CreatePodcastEpisodeSerializer,
    CreatePodcastSeasonSerializer,
    CreateVoxPopEpisodeSerializer,
    CreateVoxPopSerializer,
    UpdatePodcastEpisodeSerializer,
    UpdatePodcastSeasonSerializer,
    UpdateVoxPopEpisodeSerializer,
    UpdateVoxPopSerializer,
)
from main.graphql.context import Info
from utils.graphql.mutations import ModelMutation
from utils.graphql.types import MutationResponseType


@strawberry.type
class Mutation:
    # Podcast Season ----------------
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_podcast_season(
        self,
        info: Info,
        data: CreatePodcastSeasonInput,
    ) -> MutationResponseType[PodcastSeasonType]:
        return await ModelMutation(CreatePodcastSeasonSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_podcast_season(
        self,
        info: Info,
        data: UpdatePodcastSeasonInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[PodcastSeasonType]:
        podcast_season = await PodcastSeason.objects.aget(pk=pk)
        return await ModelMutation(UpdatePodcastSeasonSerializer).handle_update_mutation(data, info, podcast_season)

    # Podcast Episode ----------------

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_podcast_episode(
        self,
        info: Info,
        data: CreatePodcastEpisodeInput,
    ) -> MutationResponseType[PodcastEpisodeType]:
        return await ModelMutation(CreatePodcastEpisodeSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_podcast_episode(
        self,
        info: Info,
        data: UpdatePodcastEpisodeInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[PodcastEpisodeType]:
        podcast_episode = await PodcastEpisode.objects.aget(pk=pk)
        return await ModelMutation(UpdatePodcastEpisodeSerializer).handle_update_mutation(data, info, podcast_episode)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def archive_podcast_episode(
        self,
        info: Info,
        pk: strawberry.ID,
    ) -> MutationResponseType[PodcastEpisodeType]:
        podcast = await PodcastEpisode.objects.aget(pk=pk)
        if podcast.is_archived:
            return MutationResponseType(ok=False, errors=["This Episode is already archived."])  # type: ignore[reportReturnType]

        podcast.is_archived = True
        await sync_to_async(podcast.save)(update_fields=["is_archived"])
        return MutationResponseType(ok=True, errors=None)  # type: ignore[reportReturnType]

    # voxPop Season ----------------
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_voxpop_season(self, info: Info, data: CreateVoxPopInput) -> MutationResponseType[VoxPopSeasonType]:
        return await ModelMutation(CreateVoxPopSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_voxpop_season(
        self,
        info: Info,
        data: UpdateVoxPopInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[VoxPopSeasonType]:
        vox_pop_season = await VoxPop.objects.aget(pk=pk)
        return await ModelMutation(UpdateVoxPopSerializer).handle_update_mutation(data, info, vox_pop_season)

    # Podcast Episode ----------------

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_voxpop_episode(
        self,
        info: Info,
        data: CreateVoxPopEpisodeInput,
    ) -> MutationResponseType[VoxPopEpisodeType]:
        return await ModelMutation(CreateVoxPopEpisodeSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_voxpop_episode(
        self,
        info: Info,
        data: UpdateVoxPopEpisodeInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[VoxPopEpisodeType]:
        vox_pop_episode = await VoxPopEpisode.objects.aget(pk=pk)
        return await ModelMutation(UpdateVoxPopEpisodeSerializer).handle_update_mutation(data, info, vox_pop_episode)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def archive_voxpop_episode(
        self,
        info: Info,
        pk: strawberry.ID,
    ) -> MutationResponseType[VoxPopEpisodeType]:
        vox_pop = await VoxPopEpisode.objects.aget(pk=pk)
        if vox_pop.is_archived:
            return MutationResponseType(ok=False, errors=["This Episode is already archived."])  # type: ignore[reportReturnType]

        vox_pop.is_archived = True
        await sync_to_async(vox_pop.save)(update_fields=["is_archived"])
        return MutationResponseType(ok=True, errors=None)  # type: ignore[reportReturnType]
