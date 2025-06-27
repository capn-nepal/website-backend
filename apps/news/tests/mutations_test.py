from apps.news.factories import NewsFactory
from apps.news.models import NewsTypeEnum, StatusEnum
from apps.user.factories import UserFactory
from main.tests.base_test import TestCase


class TestNewsMutation(TestCase):
    class Mutation:
        CREATE_NEWS = """
          mutation CreateNews($data: CreateNewsInput!) {
            createNews(data: $data) {
              ... on NewsTypeMutationResponseType {
                errors
                result {
                  id
                  title
                  description
                  newsType
                  publishedDate
                  status
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

        UPDATE_NEWS = """
          mutation UpdateNews($pk: ID!, $data: UpdateNewsInput!) {
            updateNews(pk: $pk, data: $data) {
              ... on NewsTypeMutationResponseType {
                errors
                result {
                  id
                  title
                  description
                  newsType
                  publishedDate
                  status
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
        cls.user = UserFactory.create(email="news_tester@example.com")

    def _create_news_mutation(self, data: dict):
        return self.query_check(
            self.Mutation.CREATE_NEWS,
            variables={"data": data},
        )

    def _update_news_mutation(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_NEWS,
            variables={
                "pk": pk,
                "data": data,
            },
        )

    def test_create_news(self):
        news_data = {
            "title": "Test News Title",
            "description": "Test news content.",
            "publishedDate": "2025-06-01",
            "newsType": NewsTypeEnum.NEWS.name,
        }

        # Without authentication
        content = self._create_news_mutation(news_data)
        assert content["data"]["createNews"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_news_mutation(news_data)
        response_data = content["data"]["createNews"]

        assert response_data["errors"] is None, content
        assert response_data["result"]["title"] == news_data["title"]
        assert response_data["result"]["description"] == news_data["description"]

    def test_update_news(self):
        news = NewsFactory.create(
            title="Title101",
            description="Initial description.",
            published_date="2025-01-01",
        )

        update_data = {
            "title": "Updated Title",
            "description": "Updated description.",
            "publishedDate": "2025-06-02",
        }

        # Without authentication
        content = self._update_news_mutation(self.gID(news.pk), update_data)
        assert content["data"]["updateNews"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._update_news_mutation(self.gID(news.pk), update_data)
        response_data = content["data"]["updateNews"]

        assert response_data["errors"] is None, content
        assert response_data["result"]["title"] == update_data["title"]
        assert response_data["result"]["description"] == update_data["description"]
        assert response_data["result"]["newsType"] == NewsTypeEnum.NEWS.label
        assert response_data["result"]["status"] == StatusEnum.DRAFT.name

        news.refresh_from_db()
        assert news.title == update_data["title"]
        assert news.description == update_data["description"]
