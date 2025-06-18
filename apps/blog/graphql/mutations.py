import strawberry
import strawberry_django
from strawberry_django.permissions import IsAuthenticated

from apps.blog.graphql.inputs import (
    AddAuthorInput,
    CreateBlogAssetsInput,
    CreateBlogInput,
    UpdateAuthorInput,
    UpdateBlogInput,
)
from apps.blog.graphql.types import AuthorType, BlogAssetsType, BlogType
from apps.blog.models import Author, Blog
from apps.blog.serializers import (
    AuthorSerializer,
    BlogAssetSerializer,
    CreateBlogSerializer,
    UpdateBlogSerializer,
)
from main.graphql.context import Info
from utils.graphql.mutations import ModelMutation
from utils.graphql.types import MutationResponseType


@strawberry.type
class Mutation:
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_blog(self, info: Info, data: CreateBlogInput) -> MutationResponseType[BlogType]:
        return await ModelMutation(CreateBlogSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_blog(
        self,
        info: Info,
        data: UpdateBlogInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[BlogType]:
        blog = await Blog.objects.aget(pk=pk)
        return await ModelMutation(UpdateBlogSerializer).handle_update_mutation(data, info, blog)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def create_blog_assets(self, info: Info, data: CreateBlogAssetsInput) -> MutationResponseType[BlogAssetsType]:
        return await ModelMutation(BlogAssetSerializer).handle_create_mutation(data, info, None)

    # Author -----------
    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def add_author(self, info: Info, data: AddAuthorInput) -> MutationResponseType[AuthorType]:
        return await ModelMutation(AuthorSerializer).handle_create_mutation(data, info, None)

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    async def update_author(
        self,
        info: Info,
        data: UpdateAuthorInput,
        pk: strawberry.ID,
    ) -> MutationResponseType[AuthorType]:
        blog = await Author.objects.aget(pk=pk)
        return await ModelMutation(AuthorSerializer).handle_update_mutation(data, info, blog)
