import logging
from dataclasses import is_dataclass

import strawberry
from asgiref.sync import sync_to_async
from django.db import models, transaction
from rest_framework import serializers

from main.graphql.context import Info

from .common import parse_input_data
from .drf import _CustomErrorType, mutation_is_not_valid
from .types import CustomErrorType, MutationResponseType

logger = logging.getLogger(__name__)


def get_serializer_context(info: Info, extra_context: dict | None):
    return {
        "graphql_info": info,
        "request": info.context.request,
        "extra_context": extra_context,
    }


class ModelMutation:
    InputType: type
    PartialInputType: type

    def __init__(
        self,
        serializer_class: type[serializers.Serializer],
    ):
        self.serializer_class = serializer_class

    @staticmethod
    @sync_to_async
    def handle_mutation(
        serializer_class,
        data,
        info,
        extra_context: dict | None,
        **kwargs,
    ) -> tuple[CustomErrorType | None, models.Model | None]:
        serializer = serializer_class(
            data=data,
            context=get_serializer_context(info, extra_context=extra_context),
            **kwargs,
        )
        if errors := mutation_is_not_valid(serializer):
            return errors, None
        try:
            with transaction.atomic():
                instance = serializer.save()
        except Exception:
            logger.error("Failed to handle mutation", exc_info=True)
            return _CustomErrorType.generate_message(), None
        return None, instance

    async def handle_create_mutation(
        self,
        data,
        info: Info,
        extra_context: dict | None = None,
    ) -> MutationResponseType:
        errors, saved_instance = await self.handle_mutation(
            self.serializer_class,
            parse_input_data(data),
            info,
            extra_context,
        )
        if errors:
            return MutationResponseType(ok=False, errors=errors)
        return MutationResponseType(result=saved_instance)

    async def handle_update_mutation(
        self,
        data,
        info: Info,
        instance: models.Model,
        extra_context: dict | None = None,
    ) -> MutationResponseType:
        errors, saved_instance = await self.handle_mutation(
            self.serializer_class,
            parse_input_data(data),
            info,
            extra_context,
            instance=instance,
            partial=True,
        )
        if errors:
            return MutationResponseType(ok=False, errors=errors)
        return MutationResponseType(result=saved_instance)


def process_input_data(data) -> dict | list:
    """
    Return dict from Strawberry Input Object
    NOTE: strawberry.asdict doesn't handle nested and strawberry.UNSET
    Related issue: https://github.com/strawberry-graphql/strawberry/issues/3265
    https://github.com/strawberry-graphql/strawberry/blob/d2c0fb4d2d363929c9ac10161884d004ab9cf555/strawberry/object_type.py#L395

    """
    # TODO: Write test
    if type(data) in [tuple, list]:
        return [process_input_data(datum) for datum in data]
    native_dict = {}
    for key, value in data.__dict__.items():
        if value == strawberry.UNSET:
            continue
        if isinstance(value, list):
            _list_value = []
            for _value in value:
                if is_dataclass(_value):
                    _list_value.append(process_input_data(_value))
                else:
                    _list_value.append(_value)
            native_dict[key] = _list_value
            continue
        if is_dataclass(value):
            native_dict[key] = process_input_data(value)
        else:
            native_dict[key] = value
    return native_dict
