import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from django.contrib.auth import login
from strawberry_django.permissions import IsAuthenticated

from apps.user.graphql.inputs import ChangePasswordInput, LoginInput
from apps.user.serializers import ChangePasswordSerializer, LoginSerializer
from main.graphql.context import Info
from utils.graphql.common import parse_input_data
from utils.graphql.mutations import (
    MutationResponseType,
    mutation_is_not_valid,
)

from .types import UserMeType


@strawberry.type
class Mutation:
    # Public --------------------
    @strawberry.mutation
    @sync_to_async
    def login(
        self,
        data: LoginInput,  # type: ignore[reportInvalidTypeForm]
        info: Info,
    ) -> MutationResponseType[UserMeType]:
        serializer = LoginSerializer(data=parse_input_data(data), context={"request": info.context.request})
        if errors := mutation_is_not_valid(serializer):
            return MutationResponseType(
                ok=False,
                errors=errors,
            )
        user = serializer.validated_data["user"]  # type: ignore[reportInvalidTypeForm]
        login(info.context.request, user)
        return MutationResponseType(
            result=user,
        )

    # Private --------------------
    logout = strawberry_django.auth.logout()

    @strawberry_django.mutation(extensions=[IsAuthenticated()])
    @sync_to_async
    def change_password(
        self,
        data: ChangePasswordInput,  # type: ignore[reportInvalidTypeForm]
        info: Info,
    ) -> MutationResponseType[UserMeType]:
        serializer = ChangePasswordSerializer(data=parse_input_data(data), context={"request": info.context.request})
        if errors := mutation_is_not_valid(serializer):
            return MutationResponseType(
                ok=False,
                errors=errors,
            )
        serializer.save()  # type: ignore[reportInvalidTypeForm]
        return MutationResponseType(
            ok=False,
            errors=errors,
        )
