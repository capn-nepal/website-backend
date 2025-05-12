import strawberry
import strawberry_django
from strawberry_django.permissions import IsAuthenticated

from apps.blog.graphql.inputs import CreateBlogAssetsInput, CreateBlogInput, UpdateBlogInput
from apps.blog.graphql.types import BlogAssetsType, BlogType
from apps.blog.models import Blog
from apps.blog.serializers import CreateBlogAssetSerializers, CreateBlogSerializers, UpdateBlogSerializers
from main.graphql.context import Info
from utils.graphql.mutations import ModelMutation
from utils.graphql.types import MutationResponseType


@strawberry.type
class Mutation:
    delete_blog: BlogType = strawberry_django.mutations.delete(extensions=[IsAuthenticated()])

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_blog(self, info: Info, data: CreateBlogInput) -> MutationResponseType[BlogType]:
        return await ModelMutation(CreateBlogSerializers).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_blog_assets(self, info: Info, data: CreateBlogAssetsInput) -> MutationResponseType[BlogAssetsType]:
        return await ModelMutation(CreateBlogAssetSerializers).handle_create_mutation(data, info, None)

    delete_blog_assets: BlogAssetsType = strawberry_django.mutations.delete(extensions=[IsAuthenticated()])

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_blog(
        self,
        info: Info,
        data: UpdateBlogInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[BlogType]:
        blog = await Blog.objects.aget(pk=pk)
        return await ModelMutation(UpdateBlogSerializers).handle_update_mutation(data, info, blog)
