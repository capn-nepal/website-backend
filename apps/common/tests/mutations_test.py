import typing
from pathlib import Path

from django.core.files.temp import NamedTemporaryFile
from PIL import Image

from apps.common.factories import (
    EventFactory,
    GalleryFactory,
    GalleryItemFactory,
    ReportFactory,
    YouTubeVideoFactory,
)
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


def image_query(
    *,
    query_check_func: typing.Callable,
    query: str,
    data: dict,
    **kwargs,
) -> dict:
    with NamedTemporaryFile(suffix=".jpg", dir=settings.TEMP_DIR) as image_file:  # type: ignore[reportIncompatibleVariableOverride]
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(image_file, "JPEG")
        image_file.seek(0)

        return query_check_func(
            query,
            variables={"data": data},
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


class TestCreateGalleryMutation(TestCase):
    class Mutation:
        CREATE_GALLERY = """
          mutation CreateGallery($data: GalleryInput!) {
            createGallery(data: $data) {
              ... on GalleryTypeMutationResponseType {
                errors
                result {
                  description
                  id
                  isArchived
                  name
                }
              }
              ... on OperationInfo {
                __typename
                messages {
                  code
                  field
                  kind
                  message
                }
              }
            }
          }
        """
        UPDATE_GALLERY = """
            mutation UpdateGallery($data: GalleryUpdateInput!, $pk: ID!) {
                updateGallery(data: $data, pk: $pk) {
                    ... on GalleryTypeMutationResponseType {
                        errors
                        result {
                          description
                          id
                          isArchived
                          name
                        }
                    }
                    ... on OperationInfo {
                        __typename
                        messages {
                            code
                            field
                            kind
                            message
                        }
                    }
                }
            }
        """

        ARCHIVE_GALLERY = """
            mutation ArchiveGallery($pk: ID!) {
                archiveGallery(pk: $pk) {
                    ... on GalleryTypeMutationResponseType {
                        errors
                    }
                    ... on OperationInfo {
                        __typename
                        messages {
                            code
                            field
                            kind
                            message
                        }
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="testgallery@example.com")

    def _create_gallery_mutation(self, data: dict):
        return self.query_check(
            self.Mutation.CREATE_GALLERY,
            variables={"data": data},
        )

    def _update_gallery_mutation(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_GALLERY,
            variables={
                "pk": pk,
                "data": data,
            },
        )

    def _archive_gallery_mutation(self, pk):
        return self.query_check(
            self.Mutation.ARCHIVE_GALLERY,
            variables={"pk": pk},
        )

    def test_create_gallery_mutation(self):
        gallery_data = {
            "name": "gallery number one",
            "description": "gallery one description",
        }

        # Without authentication
        content = self._create_gallery_mutation(gallery_data)
        assert content["data"]["createGallery"]["messages"] == [
            {
                "code": None,
                "field": "createGallery",
                "kind": "PERMISSION",
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_gallery_mutation(gallery_data)
        response_data = content["data"]["createGallery"]

        assert response_data["errors"] is None, content
        assert response_data["result"]["name"] == gallery_data["name"]
        assert response_data["result"]["description"] == gallery_data["description"]
        assert response_data["result"]["isArchived"] is False

    def test_update_gallery_mutation(self):
        gallery = GalleryFactory.create(
            name="gallelllllry",
            description="galleryyyy description",
        )
        updated_gallery_data = {
            "name": "updated gallelllllry",
            "description": "updated galleryyyy description",
        }
        # Without authentication
        content = self._update_gallery_mutation(self.gID(gallery.pk), updated_gallery_data)
        assert content["data"]["updateGallery"]["messages"] == [
            {
                "code": None,
                "field": "updateGallery",
                "kind": "PERMISSION",
                "message": "User is not authenticated.",
            },
        ], content
        # With authentication
        self.force_login(self.user)
        content = self._update_gallery_mutation(self.gID(gallery.pk), updated_gallery_data)
        response_data = content["data"]["updateGallery"]
        assert response_data["errors"] is None, content
        assert response_data["result"]["name"] == updated_gallery_data["name"]
        assert response_data["result"]["description"] == updated_gallery_data["description"]
        assert response_data["result"]["id"] == self.gID(gallery.pk)

    def test_archive_gallery_mutation(self):
        gallery = GalleryFactory.create(
            name="gallery name",
            description="gallery descccc",
            is_archived=False,
        )
        # Without authentication
        content = self._archive_gallery_mutation(self.gID(gallery.pk))
        assert content["data"]["archiveGallery"]["messages"] == [
            {
                "code": None,
                "field": "archiveGallery",
                "kind": "PERMISSION",
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._archive_gallery_mutation(self.gID(gallery.pk))
        resp_data = content["data"]["archiveGallery"]
        assert resp_data["errors"] is None, content
        gallery.refresh_from_db()
        assert gallery.is_archived is True


class TestGalleryItemMutations(TestCase):
    class Mutation:
        ADD_GALLERY_ITEM = """
            mutation AddGalleryItem($data: GalleryItemInput!) {
                addGalleryItem(data: $data) {
                    ... on GalleryItemTypeMutationResponseType {
                        errors
                        result {
                            caption
                            id
                            isArchived
                            gallery {
                                id
                            }
                        }
                    }
                    ... on OperationInfo {
                        __typename
                        messages {
                            code
                            field
                            kind
                            message
                        }
                    }
                }
            }
        """

        UPDATE_GALLERY_ITEM = """
            mutation UpdateGalleryItem($data: GalleryItemUpdateInput!, $pk: ID!) {
                updateGalleryItem(data: $data, pk: $pk) {
                    ... on GalleryItemTypeMutationResponseType {
                        errors
                        result {
                            caption
                            id
                            isArchived
                            gallery {
                                id
                            }
                            image {
                                url
                            }
                        }
                    }
                    ... on OperationInfo {
                        __typename
                        messages {
                            code
                            kind
                            field
                            message
                        }
                    }
                }
            }
        """

        ARCHIVE_GALLERY_ITEM = """
            mutation ArchiveGalleryItem($pk: ID!) {
                archiveGalleryItem(pk: $pk) {
                    ... on GalleryItemTypeMutationResponseType {
                        errors
                    }
                    ... on OperationInfo {
                        __typename
                        messages {
                            code
                            kind
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
        cls.user = UserFactory.create(email="testuseritem@example.com")
        cls.gallery = GalleryFactory.create(
            name="Test Gallery",
            description="Desc",
        )

    def _add_gallery_item(self, data: dict, **kwargs):
        return image_query(
            query_check_func=self.query_check,
            query=self.Mutation.ADD_GALLERY_ITEM,
            data=data,
        )

    def _update_gallery_item(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_GALLERY_ITEM,
            variables={
                "pk": pk,
                "data": data,
            },
        )

    def _archive_gallery_item(self, pk):
        return self.query_check(
            self.Mutation.ARCHIVE_GALLERY_ITEM,
            variables={"pk": pk},
        )

    def test_add_gallery_item(self):
        data = {
            "caption": "Test Caption",
            "gallery": self.gID(self.gallery.pk),
        }
        # Without auth
        content = self._add_gallery_item(data)
        assert content["data"]["addGalleryItem"]["messages"] == [
            {
                "code": None,
                "field": "addGalleryItem",
                "kind": "PERMISSION",
                "message": "User is not authenticated.",
            },
        ], content
        # With auth
        self.force_login(self.user)
        content = self._add_gallery_item(data)
        result = content["data"]["addGalleryItem"]["result"]
        assert result["caption"] == data["caption"]
        assert result["gallery"]["id"] == self.gID(self.gallery.pk)
        self.gallery_item_id = result["id"]

    def test_update_gallery_item(self):
        item = GalleryItemFactory.create(
            caption="captionnnnnn",
            is_archived=False,
            gallery=self.gallery,
        )
        update_data = {
            "caption": "Updated caption",
        }
        self.force_login(self.user)
        content = self._update_gallery_item(self.gID(item.pk), update_data)
        response_data = content["data"]["updateGalleryItem"]
        assert response_data["result"]["gallery"]["id"] == self.gID(self.gallery.pk)
        assert response_data["result"]["image"]["url"] is not None
        assert response_data["result"]["caption"] == update_data["caption"]

    def test_archive_gallery_item_mutation(self):
        item = GalleryItemFactory.create(
            caption="Caption2",
            is_archived=False,
            gallery=self.gallery,
        )
        # Without authentication
        content = self._archive_gallery_item(self.gID(item.pk))
        assert content["data"]["archiveGalleryItem"]["messages"] == [
            {
                "code": None,
                "field": "archiveGalleryItem",
                "kind": "PERMISSION",
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._archive_gallery_item(self.gID(item.pk))
        resp_data = content["data"]["archiveGalleryItem"]
        assert resp_data["errors"] is None, content
        item.refresh_from_db()
        assert item.is_archived is True


class TestArtworkMutations(TestCase):
    class Mutation:
        CREATE_ARTWORK = """
        mutation CreateArtwork($data: ArtworkInput!) {
            createArtwork(data: $data) {
                ... on ArtworkTypeMutationResponseType {
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
                        code
                        field
                        kind
                        message
                    }
                }
            }
        }
    """

        DELETE_ARTWORK = """
        mutation DeleteArtwork($data: ArtWorkDeleteInput!) {
            deleteArtwork(data: $data) {
                ... on OperationInfo {
                    __typename
                    messages {
                        code
                        field
                        kind
                        message
                    }
                }
            }
        }
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="artwork@example.com")

    def _create_artwork(self, data: dict, **kwargs):
        return image_query(
            query_check_func=self.query_check,
            query=self.Mutation.CREATE_ARTWORK,
            data=data,
        )

    def _delete_artwork(self, artwork_id: str):
        return self.query_check(
            self.Mutation.DELETE_ARTWORK,
            variables={
                "data": {
                    "id": artwork_id,
                },
            },
        )

    def test_create_artwork_mutation(self):
        artwork = {"name": "artwork-1"}
        # Without authentication
        content = self._create_artwork(artwork)
        assert content["data"]["createArtwork"]["messages"] == [
            {
                "code": None,
                "field": "createArtwork",
                "kind": "PERMISSION",
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_artwork(artwork)
        result = content["data"]["createArtwork"]["result"]
        assert result["name"] == artwork["name"]
        assert result["id"] is not None
        assert result["image"]["url"] is not None
