from apps.common.factories import EventFactory, ReportFactory
from apps.user.factories import UserFactory
from main.tests.base_test import TestCase


class TestEventMutation(TestCase):
    class Mutation:
        CREATE_EVENT = """
          mutation CreateEvent($data: CreateEventInput!) {
            createEvent(data: $data) {
              ... on EventTypeMutationResponseType {
                errors
                ok
                result {
                  id
                  name
                  description
                  startDate
                  endDate
                  location
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
        UPDATE_EVENT = """
        mutation UpdateEvent($pk: ID!, $data: UpdateEventInput!) {
          updateEvent(pk: $pk, data: $data) {
            ... on EventTypeMutationResponseType {
              errors
              ok
              result {
                id
                name
                description
                startDate
                endDate
                location
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
        ARCHIVE_EVENT = """
          mutation ArchiveEvent($pk: ID!) {
            archiveEvent(pk: $pk) {
              ... on EventTypeMutationResponseType {
                errors
                ok
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
        cls.user = UserFactory.create(email="testuser@example.com")

    def _create_event_mutation(self, event_data: dict, **kwargs):
        return self.query_check(
            self.Mutation.CREATE_EVENT,
            variables={"data": event_data},
            **kwargs,
        )

    def _update_event_mutation(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_EVENT,
            variables={
                "pk": pk,
                "data": data,
            },
        )

    def _archive_event_mutation(self, pk):
        return self.query_check(
            self.Mutation.ARCHIVE_EVENT,
            variables={"pk": pk},
        )

    def test_create_event(self):
        event_data = {
            "name": "Test Event",
            "description": "Sample event",
            "startDate": "2025-06-01",
            "endDate": "2025-06-02",
            "location": "KTM",
        }

        # Without authentication
        content = self._create_event_mutation(event_data)
        assert content["data"]["createEvent"]["messages"] == [
            {
                "code": None,
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_event_mutation(event_data)

        response_data = content["data"]["createEvent"]
        assert response_data["errors"] is None, content
        assert response_data["ok"] is True
        assert response_data["result"]["name"] == "Test Event"
        assert response_data["result"]["location"] == "KTM"
        assert response_data["result"]["endDate"] == "2025-06-02"
        assert response_data["result"]["startDate"] == "2025-06-01"

    def test_update_event(self):
        event = EventFactory.create(
            name="Test Event",
            description="Sample event",
            start_date="2025-06-01",
            end_date="2025-06-02",
            location="KTM",
        )

        update_event_data = {
            "name": "Updated Event",
            "description": "Updated description",
            "startDate": "2025-07-01",
            "endDate": "2025-07-02",
            "location": "BKT",
        }

        # Without authentication
        content = self._update_event_mutation(self.gID(event.pk), update_event_data)
        assert content["data"]["updateEvent"]["messages"] == [
            {
                "code": None,
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._update_event_mutation(self.gID(event.pk), update_event_data)
        resp_data = content["data"]["updateEvent"]
        assert resp_data["errors"] is None, content

        event.refresh_from_db()
        assert resp_data == self.g_mutation_response(
            ok=True,
            result=dict(
                id=self.gID(event.pk),
                name=event.name,
                description=event.description,
                startDate=str(event.start_date),
                endDate=str(event.end_date),
                location=event.location,
            ),
        ), content

    def test_archive_event(self):
        event = EventFactory.create(
            name="Archive Me",
            description="To be archived",
            start_date="2025-08-01",
            end_date="2025-08-02",
            location="PKR",
        )

        # Without authentication
        content = self._archive_event_mutation(self.gID(event.pk))
        assert content["data"]["archiveEvent"]["messages"] == [
            {
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._archive_event_mutation(self.gID(event.pk))
        resp_data = content["data"]["archiveEvent"]

        assert resp_data["errors"] is None, content
        assert resp_data["ok"] is True, content

        event.refresh_from_db()
        assert event.is_deleted is True


class TestReportMutations(TestCase):
    class Mutation:
        CREATE_REPORT = """
          mutation createReport($data: CreateReportInput!) {
            createReport(data: $data) {
              ... on ReportTypeMutationResponseType {
                errors
                ok
                result {
                  id
                  title
                  description
                  publishedDate
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
        UPDATE_REPORT = """
        mutation UpdateReport($pk: ID!, $data: UpdateReportInput!) {
          updateReport(pk: $pk, data: $data) {
            ... on ReportTypeMutationResponseType {
              errors
              ok
              result {
                id
                title
                description
                publishedDate
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
        ARCHIVE_REPORT = """
          mutation ArchiveReport($pk: ID!) {
            archiveReport(pk: $pk) {
              ... on ReportTypeMutationResponseType {
                errors
                ok
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
        cls.user = UserFactory.create(email="testreport@example.com")

    def _update_report_mutation(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_REPORT,
            variables={
                "pk": pk,
                "data": data,
            },
        )

    def _archive_report_mutation(self, pk):
        return self.query_check(
            self.Mutation.ARCHIVE_REPORT,
            variables={"pk": pk},
        )

    def test_update_report(self):
        report = ReportFactory.create(
            title="report000",
            description="ddddddd",
            published_date="2025-08-01",
        )
        update_report_data = {
            "title": "Updated report",
            "description": "Updated description",
            "publishedDate": "2025-07-01",
        }

        # Without authentication
        content = self._update_report_mutation(self.gID(report.pk), update_report_data)
        assert content["data"]["updateReport"]["messages"] == [
            {
                "code": None,
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._update_report_mutation(self.gID(report.pk), update_report_data)
        resp_data = content["data"]["updateReport"]
        assert resp_data["errors"] is None, content

        report.refresh_from_db()
        assert resp_data == self.g_mutation_response(
            ok=True,
            result=dict(
                id=self.gID(report.pk),
                title=report.title,
                description=report.description,
                publishedDate=str(report.published_date),
            ),
        ), content

    def test_archive_report(self):
        report = ReportFactory.create(
            title="report000",
            description="ddddddd",
            published_date="2025-08-01",
        )

        # Without authentication
        content = self._archive_report_mutation(self.gID(report.pk))
        assert content["data"]["archiveReport"]["messages"] == [
            {
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._archive_report_mutation(self.gID(report.pk))
        resp_data = content["data"]["archiveReport"]
        assert resp_data["errors"] is None, content
        assert resp_data["ok"] is True, content
        report.refresh_from_db()
        assert report.is_deleted is True
