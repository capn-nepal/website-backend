import typing
from pathlib import Path

from django.core.files.temp import NamedTemporaryFile
from PIL import Image

from apps.common.factories import (
    EventFactory,
    ReportFactory,
    YouTubeVideoFactory,
)
from apps.common.models import ImageTypeEnum
from apps.user.factories import UserFactory
from main import settings
from main.tests.base_test import TestCase

BASE_DIR = Path(__file__).resolve().parent


def youtube_video_query(
    *,
    query_check_func: typing.Callable,
    query: str,
    video_data: dict,
    **kwargs,
) -> dict:
    with NamedTemporaryFile(suffix=".jpg", dir=settings.TEMP_DIR) as image_file:  # type: ignore[reportIncompatibleVariableOverride]
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(image_file, "JPEG")
        image_file.seek(0)

        return query_check_func(
            query,
            variables={"data": video_data},
            files={"thumbnail": image_file},
            map={"thumbnail": ["variables.data.thumbnail"]},
            **kwargs,
        )


def gallery_item_query(
    *,
    query_check_func: typing.Callable,
    query: str,
    image_data: dict,
    **kwargs,
) -> dict:
    with NamedTemporaryFile(suffix=".jpg", dir=settings.TEMP_DIR) as image_file:  # type: ignore[reportIncompatibleVariableOverride]
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(image_file, "JPEG")
        image_file.seek(0)

        return query_check_func(
            query,
            variables={"data": image_data},
            files={"image": image_file},
            map={"image": ["variables.data.image"]},
            **kwargs,
        )


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


class TestYouTubeVideoMutation(TestCase):
    class Mutation:
        CREATE_YOUTUBE_VIDEO = """
          mutation AddYouTubeVideo($data: YoutubeVideoInput!) {
            addYoutubeVideo(data: $data) {
              ... on YouTubeVideoTypeMutationResponseType {
                errors
                result {
                  id
                  title
                  videoUrl
                  isArchived
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

        UPDATE_YOUTUBE_VIDEO = """
          mutation UpdateYouTubeVideo($pk: ID!, $data: UpdateYoutubeVideoInput!) {
            updateYoutubeVideo(pk: $pk, data: $data) {
              ... on YouTubeVideoTypeMutationResponseType {
                errors
                result {
                  id
                  title
                  videoUrl
                  isArchived
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
        ARCHIVE_YOUTUBE_VIDEO = """
          mutation ArchiveYouTubeVideo($pk: ID!) {
            archiveYoutubeVideo(pk: $pk) {
              ... on YouTubeVideoTypeMutationResponseType {
                errors
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
        cls.user = UserFactory.create(email="testuser1234@example.com")

    def _create_video_mutation(self, video_data: dict, **kwargs):
        return youtube_video_query(
            query_check_func=self.query_check,
            query=self.Mutation.CREATE_YOUTUBE_VIDEO,
            video_data=video_data,
        )

    def _update_video_mutation(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_YOUTUBE_VIDEO,
            variables={
                "pk": pk,
                "data": data,
            },
        )

    def _archive_video_mutation(self, pk):
        return self.query_check(
            self.Mutation.ARCHIVE_YOUTUBE_VIDEO,
            variables={"pk": pk},
        )

    def test_create_youtube_video(self):
        video_data = {
            "title": "Test Video",
            "videoUrl": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "releaseDate": "2025-06-01",
        }

        # Without authentication
        content = self._create_video_mutation(video_data)
        assert content["data"]["addYoutubeVideo"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_video_mutation(video_data)
        response_data = content["data"]["addYoutubeVideo"]

        assert response_data["errors"] is None, content
        assert response_data["result"]["title"] == "Test Video"
        assert response_data["result"]["videoUrl"] == video_data["videoUrl"]
        assert response_data["result"]["isArchived"] is False

    def test_update_youtube_video(self):
        video = YouTubeVideoFactory.create(
            title="capn video",
            video_url="https://old.url",
            release_date="2025-01-01",
            is_archived=False,
        )

        update_data = {
            "title": "Updated Video",
            "videoUrl": "https://updated.url",
            "releaseDate": "2025-06-02",
        }

        # Without authentication
        content = self._update_video_mutation(self.gID(video.pk), update_data)
        assert content["data"]["updateYoutubeVideo"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._update_video_mutation(self.gID(video.pk), update_data)
        response_data = content["data"]["updateYoutubeVideo"]

        assert response_data["errors"] is None, content
        assert response_data["result"]["title"] == update_data["title"]
        assert response_data["result"]["videoUrl"] == update_data["videoUrl"]
        assert response_data["result"]["id"] == self.gID(video.pk)
        assert response_data["result"]["isArchived"] is False

        video.refresh_from_db()
        assert video.title == update_data["title"]
        assert video.video_url == update_data["videoUrl"]

    def test_archive_youtube_video(self):
        video = YouTubeVideoFactory.create(
            title="capn video",
            video_url="https://old.url",
            release_date="2025-01-01",
            is_archived=False,
        )
        # Without authentication
        content = self._archive_video_mutation(self.gID(video.pk))
        assert content["data"]["archiveYoutubeVideo"]["messages"] == [
            {
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._archive_video_mutation(self.gID(video.pk))
        resp_data = content["data"]["archiveYoutubeVideo"]
        assert resp_data["errors"] is None, content

        video.refresh_from_db()
        assert video.is_archived is True


class TestGalleryItemMutation(TestCase):
    class Mutation:
        ADD_GALLERY_ITEM = """
          mutation AddGalleryItem($data: GalleryItemInput!) {
            addGalleryItem(data: $data) {
              ... on GalleryItemTypeMutationResponseType {
                errors
                result {
                  id
                  imageType
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
        cls.user = UserFactory.create(email="testuser1234@example.com")

    def _create_gallery_item(self, image_data: dict, **kwargs):
        return gallery_item_query(
            query_check_func=self.query_check,
            query=self.Mutation.ADD_GALLERY_ITEM,
            image_data=image_data,
            **kwargs,
        )

    def test_add_gallery_item(self):
        image_data = {
            "imageType": ImageTypeEnum.ARTWORK.name,
        }

        # Without authentication
        content = self._create_gallery_item(image_data)
        assert content["data"]["addGalleryItem"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_gallery_item(image_data)
        response_data = content["data"]["addGalleryItem"]

        assert response_data["errors"] is None, content
        assert response_data["result"]["imageType"] == ImageTypeEnum.ARTWORK
