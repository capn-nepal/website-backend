from apps.blog.factories import AuthorFactory, BlogFactory
from apps.user.factories import UserFactory
from main.tests.base_test import TestCase


class TestBlogQuery(TestCase):
    class Query:
        BLOGS = """
            query blogs($pagination: OffsetPaginationInput, $order: BlogOrder) {
                blogs(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        id
                        content
                        description
                        featured
                        title
                        publishedDate
                        author {
                            id
                        }
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="user1@gmail.com")
        cls.user_resource_kwargs = dict(
            created_by=cls.user,
            modified_by=cls.user,
        )
        cls.author = AuthorFactory.create(name="hero")
        cls.blogs = [
            BlogFactory.create(
                created_by=cls.user,
                title="Test Blog 1",
                author=cls.author,
                content="Content 1",
                description="Description 1",
                featured=True,
                published_date="2025-01-01",
            ),
            BlogFactory.create(
                created_by=cls.user,
                title="Test Blog 2",
                author=cls.author,
                content="Content 2",
                description="Description 2",
                featured=True,
                published_date="2025-01-02",
            ),
        ]

    def test_blogs_query(self):
        def _query():
            return self.query_check(
                self.Query.BLOGS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        content = _query()

        expected_results = [
            dict(
                id=self.gID(blog.pk),
                title=blog.title,
                content=blog.content,
                description=blog.description,
                featured=blog.featured,
                publishedDate=str(blog.published_date),
                author={"id": str(blog.author.id)},
            )
            for blog in sorted(self.blogs, key=lambda b: b.pk)  # Match ASC order
        ]

        assert content["data"]["blogs"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=expected_results,
            ),
        }, content
