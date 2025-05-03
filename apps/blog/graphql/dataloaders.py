import typing

from asgiref.sync import sync_to_async
from django.utils.functional import cached_property
from strawberry.dataloader import DataLoader

from apps.common.graphql.dataloaders import load_model_objects
from apps.blog.models import Blog

if typing.TYPE_CHECKING:
    from .types import BlogType


def load_blog(keys: list[int]) -> list["BlogType"]:
    return load_model_objects(Blog, keys)  # type: ignore[reportReturnType]


class BlogDataLoader:
    # FIXME: Not used
    @cached_property
    def load_blog(self):
        return DataLoader(load_fn=sync_to_async(load_blog))
