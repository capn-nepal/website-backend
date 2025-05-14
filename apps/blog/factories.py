import factory
from factory.django import DjangoModelFactory

from apps.blog.models import Author, Blog, BlogAsset
from apps.user.factories import UserFactory


class AuthorFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = Author


class BlogFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    author = factory.SubFactory(AuthorFactory)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = Blog


class BlogAssetsFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    blog = factory.SubFactory(BlogFactory)

    class Meta:  # type: ignore[reportIncompatibleVariableOverride]
        model = BlogAsset
