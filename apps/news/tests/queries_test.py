from apps.news.factories import NewsFactory
from apps.news.models import NewsTypeEnum, StatusEnum
from apps.user.factories import UserFactory
from main.tests.base_test import TestCase


class TestNewsQuery(TestCase):
    class Query:
        NEWS = """
          query news($pagination: OffsetPaginationInput, $order: NewsOrder) {
            news(pagination: $pagination, order: $order) {
              totalCount
              results {
                id
                title
                description
                newsType
                status
              }
              pageInfo {
                limit
                offset
              }
            }
          }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="newsuser@gmail.com")

    def test_news_query(self):
        def _query():
            return self.query_check(
                self.Query.NEWS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        news_items = [
            NewsFactory.create(
                title="Breaking News One",
                description="Something",
                published_date="2025-06-01",
            ),
            NewsFactory.create(
                title="Breaking News Two",
                description="Something2",
                published_date="2025-06-01",
            ),
        ]

        content = _query()
        assert content["data"]["news"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    dict(
                        id=self.gID(news.id),
                        title=news.title,
                        description=news.description,
                        newsType=NewsTypeEnum.NEWS.name,
                        status=StatusEnum.DRAFT.name,
                    )
                    for news in news_items
                ],
            ),
        }, content
