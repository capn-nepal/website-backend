import typing
from pathlib import Path

from django.core.files.temp import NamedTemporaryFile
from PIL import Image

from apps.blog.factories import AuthorFactory, BlogFactory
from apps.blog.models import Author, Blog, BlogAsset
from apps.user.factories import UserFactory
from main import settings
from main.tests.base_test import TestCase

BASE_DIR = Path(__file__).resolve().parent


def create_blog_query(
    *,
    query_check_func: typing.Callable,
    query: str,
    blog_data: dict,
    **kwargs,
) -> dict:
    with NamedTemporaryFile(suffix=".jpg", dir=settings.TEMP_DIR) as image_file:  # type: ignore[reportIncompatibleVariableOverride]
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(image_file, "JPEG")
        image_file.seek(0)

        return query_check_func(
            query,
            variables={"data": blog_data},
            files={"coverImage": image_file},
            map={"coverImage": ["variables.data.coverImage"]},
            **kwargs,
        )


def update_blog_query(
    *,
    query_check_func: typing.Callable,
    query: str,
    pk: str,
    blog_data: dict,
    **kwargs,
) -> dict:
    return query_check_func(
        query,
        variables={
            "pk": pk,
            "data": blog_data,
        },
        **kwargs,
    )


def create_blog_asset_query(
    *,
    query_check_func: typing.Callable,
    query: str,
    project_asset_data: dict,
    **kwargs,
) -> dict:
    with (
        NamedTemporaryFile(dir=settings.TEMP_DIR, suffix=".jpeg") as test_file,  # type: ignore[reportIncompatibleVariableOverride]
    ):
        # Mock image
        test_file.write(b"l")
        test_file.seek(0)

        return query_check_func(
            query,
            variables={
                "data": project_asset_data,
            },
            files={
                "testFile": test_file,
            },
            map={
                "testFile": ["variables.data.file"],
            },
            **kwargs,
        )


def add_author_query(
    *,
    query_check_func: typing.Callable,
    query: str,
    author_data: dict,
    **kwargs,
) -> dict:
    with NamedTemporaryFile(suffix=".jpg", dir=settings.TEMP_DIR) as image_file:  # type: ignore[reportIncompatibleVariableOverride]
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(image_file, "JPEG")
        image_file.seek(0)

        return query_check_func(
            query,
            variables={"data": author_data},
            files={"image": image_file},
            map={"image": ["variables.data.image"]},
            **kwargs,
        )


def update_author_query(
    *,
    query_check_func: typing.Callable,
    query: str,
    pk: str,
    author_data: dict,
    **kwargs,
) -> dict:
    return query_check_func(
        query,
        variables={
            "pk": pk,
            "data": author_data,
        },
        **kwargs,
    )


class TestBlogMutation(TestCase):
    class Mutation:
        CREATE_BLOG = """
            mutation CreateBlog($data: CreateBlogInput!) {
              createBlog(data: $data) {
                ... on BlogTypeMutationResponseType {
                  errors
                  ok
                  result {
                    id
                    title
                    content
                    description
                    featured
                    publishedDate
                  }
                }
                ... on OperationInfo {
                  __typename
                  messages {
                    code
                    field
                    message
                  }
                }
              }
            }
        """
        UPDATE_BLOG = """
        mutation UpdateBlog($pk: ID!, $data: UpdateBlogInput!) {
          updateBlog(pk: $pk, data: $data) {
            ... on BlogTypeMutationResponseType {
              errors
              ok
              result {
                id
                title
                content
                description
                featured
                publishedDate
              }
            }
            ... on OperationInfo {
              __typename
              messages {
                code
                field
                message
              }
            }
          }
        }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="test@gmail.com")
        cls.user_resource_kwargs = dict(
            created_by=cls.user,
            modified_by=cls.user,
        )
        cls.author = AuthorFactory.create(name="john")

    def _create_blog_mutation(self, blog_data: dict, **kwargs):
        return create_blog_query(
            query_check_func=self.query_check,
            query=self.Mutation.CREATE_BLOG,
            blog_data=blog_data,
        )

    def _update_blog_mutation(self, pk: str, blog_data: dict, **kwargs):
        return update_blog_query(
            query_check_func=self.query_check,
            query=self.Mutation.UPDATE_BLOG,
            pk=pk,
            blog_data=blog_data,
            **kwargs,
        )

    def test_create_blog(self):
        blog_data = {
            "title": "Test Blog",
            "description": "Sample description",
            "content": "Sample blog content",
            "featured": True,
            "publishedDate": "2025-01-01",
            "author": self.author.pk,
        }

        # Without authentication
        content = self._create_blog_mutation(blog_data)
        assert content["data"]["createBlog"]["messages"] == [
            {
                "code": None,
                "field": "createBlog",
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_blog_mutation(blog_data)

        response_data = content["data"]["createBlog"]
        assert response_data["errors"] is None, content

        # Check blog in database
        blog = Blog.objects.get(pk=response_data["result"]["id"])
        assert response_data == self.g_mutation_response(
            ok=True,
            result=dict(
                id=self.gID(blog.pk),
                title=blog.title,
                content=blog.content,
                description=blog.description,
                publishedDate=str(blog.published_date),
                featured=blog.featured,
            ),
        ), content

    def test_update_blog(self):
        blog = BlogFactory.create(
            **self.user_resource_kwargs,
            title="new Blog",
            description="new desc",
            content="new content",
            published_date="2025-02-01",
            featured=False,
            author=self.author,
        )
        blog_data = {
            "title": "Updated Blog",
            "description": "Updated desc",
            "content": "Updated content",
            "publishedDate": "2025-02-02",
            "featured": True,
        }
        #  Without authentication
        content = self._update_blog_mutation(str(blog.pk), blog_data)
        assert content["data"]["updateBlog"]["messages"] == [
            {
                "code": None,
                "field": "updateBlog",
                "message": "User is not authenticated.",
            },
        ], content

        #  With authentication
        self.force_login(self.user)
        content = self._update_blog_mutation(str(blog.pk), blog_data)
        resp_data = content["data"]["updateBlog"]
        assert resp_data["errors"] is None, content

        blog.refresh_from_db()
        assert resp_data == self.g_mutation_response(
            ok=True,
            result=dict(
                id=self.gID(blog.pk),
                title=blog.title,
                content=blog.content,
                description=blog.description,
                publishedDate=str(blog.published_date),
                featured=blog.featured,
            ),
        ), content


class TestBlogAssetsMutation(TestCase):
    class Mutation:
        CREATE_BLOG_ASSET = """
        mutation CreateBlogAsset($data: CreateBlogAssetsInput!) {
            createBlogAssets(data: $data) {
                ... on BlogAssetsTypeMutationResponseType {
                    errors
                    ok
                    result {
                        id
                        file {
                            name
                        }
                        blog {
                            pk
                        }
                    }
                }
                ... on OperationInfo {
                    __typename
                    messages {
                        code
                        message
                    }
                }
            }
        }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="blog-assets@test.com")
        cls.author = AuthorFactory.create(name="name")
        cls.blog = BlogFactory.create(
            author=cls.author,
            created_by=cls.user,
            modified_by=cls.user,
            published_date="2025-02-01",
        )

    def _create_blog_asset(self, blog_asset_data: dict, **kwargs):
        return create_blog_asset_query(
            query_check_func=self.query_check,
            query=self.Mutation.CREATE_BLOG_ASSET,
            project_asset_data=blog_asset_data,
            **kwargs,
        )

    def test_create_blog_asset(self):
        blog_asset_data = {
            "blog": (self.blog.pk),
        }
        # Without authentication
        content = self._create_blog_asset(blog_asset_data)
        assert content["data"]["createBlogAssets"]["messages"] == [
            {
                "code": None,
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_blog_asset(blog_asset_data)
        response_data = content["data"]["createBlogAssets"]
        assert response_data["errors"] is None, content
        assert response_data["ok"] is True, content

        blog_asset = BlogAsset.objects.get(pk=response_data["result"]["id"])
        assert blog_asset.blog == self.blog


class TestAuthorMutations(TestCase):
    class Mutation:
        ADD_AUTHOR = """
                mutation addAuthor($data: AddAuthorInput!) {
                    addAuthor(data: $data) {
                        ... on AuthorTypeMutationResponseType {
                            ok
                            errors
                            result {
                                id
                                name
                                image {
                                    url
                                }
                            }
                        }
                        ... on OperationInfo {
                            __typename
                            messages {
                                message
                            }
                        }
                    }
                }
            """
        UPDATE_AUTHOR = """
            mutation updateAuthor($pk: ID!, $data: UpdateAuthorInput!) {
                updateAuthor(pk: $pk, data: $data) {
                    ... on AuthorTypeMutationResponseType {
                        ok
                        errors
                        result {
                            id
                            name
                            image {
                                url
                            }
                        }
                    }
                    ... on OperationInfo {
                        __typename
                        messages {
                            message
                        }
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="user221@gmail.com")
        cls.author = AuthorFactory.create(name="hero")

    def _add_author_mutation(self, author_data: dict, **kwargs):
        return add_author_query(
            query_check_func=self.query_check,
            query=self.Mutation.ADD_AUTHOR,
            author_data=author_data,
            **kwargs,
        )

    def _update_author_mutation(self, pk: str, author_data: dict, **kwargs):
        return update_author_query(
            query_check_func=self.query_check,
            query=self.Mutation.UPDATE_AUTHOR,
            pk=pk,
            author_data=author_data,
            **kwargs,
        )

    def test_add_author_mutation(self):
        author_data = {
            "name": "Test Author",
        }
        # Without authentication
        content = self._add_author_mutation(author_data)
        assert content["data"]["addAuthor"]["messages"] == [
            {
                "message": "User is not authenticated.",
            },
        ], content
        # With authentication
        self.force_login(self.user)
        content = self._add_author_mutation(author_data)
        response_data = content["data"]["addAuthor"]
        assert response_data["errors"] is None, content
        author = Author.objects.get(pk=response_data["result"]["id"])
        assert response_data == self.g_mutation_response(
            ok=True,
            result=dict(
                id=self.gID(author.pk),
                name=author.name,
                image=dict(url=author.image.url if author.image else None),
            ),
        ), content

    def test_update_author(self):
        author = AuthorFactory.create(
            name="Test Author2",
        )
        author_data = {
            "name": "Updated Author",
        }
        #  Without authentication
        content = self._update_author_mutation(str(author.pk), author_data)
        assert content["data"]["updateAuthor"]["messages"] == [
            {
                "message": "User is not authenticated.",
            },
        ], content

        #  With authentication
        self.force_login(self.user)
        content = self._update_author_mutation(str(author.pk), author_data)
        resp_data = content["data"]["updateAuthor"]
        assert resp_data["ok"] is True, content
        assert resp_data["errors"] is None, content

        author.refresh_from_db()
        assert resp_data == self.g_mutation_response(
            ok=True,
            result=dict(
                id=self.gID(author.pk),
                name=author.name,
                image=None,
            ),
        ), content
