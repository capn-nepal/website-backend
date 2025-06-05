import strawberry
import strawberry_django
from strawberry_django.permissions import IsAuthenticated

from apps.news.graphql.inputs import CreateNewsInput, UpdateNewsInput
from apps.news.graphql.types import NewsType
from apps.news.models import News
from apps.news.serializers import CreateNewsSerializer, UpdateNewsSerializer
from main.graphql.context import Info
from utils.graphql.mutations import ModelMutation
from utils.graphql.types import MutationResponseType


@strawberry.type
class Mutation:
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_news(self, info: Info, data: CreateNewsInput) -> MutationResponseType[NewsType]:
        return await ModelMutation(CreateNewsSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_news(
        self,
        info: Info,
        data: UpdateNewsInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[NewsType]:
        event = await News.objects.aget(pk=pk)
        return await ModelMutation(UpdateNewsSerializer).handle_update_mutation(data, info, event)
