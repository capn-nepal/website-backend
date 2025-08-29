from apps.common.factories import (
    ArtworkFactory,
    ChangemakerFactory,
    EventFactory,
    GalleryFactory,
    GalleryItemFactory,
    ReportFactory,
    YouTubeVideoFactory,
)
from apps.user.factories import UserFactory
from main.tests.base_test import TestCase


class TestReportQuery(TestCase):
    class Query:
        REPORTS = """
            query reports($pagination: OffsetPaginationInput, $order: ReportOrder) {
                reports(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        id
                        title
                        description
                        publishedDate
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
        cls.reports = [
            ReportFactory.create(
                title="test report 1",
                description="Description 1",
                published_date="2025-01-01",
            ),
            ReportFactory.create(
                title="test report 1",
                description="Description 1",
                published_date="2025-01-01",
            ),
        ]

    def test_report_query(self):
        def _query():
            return self.query_check(
                self.Query.REPORTS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        content = _query()
        assert content["data"]["reports"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    dict(
                        id=self.gID(report.pk),
                        title=report.title,
                        description=report.description,
                        publishedDate=str(report.published_date),
                    )
                    for report in self.reports
                ],
            ),
        }, content


class TestEventQuery(TestCase):
    class Query:
        EVENTS = """
             query events($pagination: OffsetPaginationInput,$order: EventOrder) {
                events(pagination: $pagination, order:$order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        id
                        name
                        description
                        location
                        startDate
                        endDate
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="user2@gmail.com")
        cls.user_resource_kwargs = dict(
            created_by=cls.user,
            modified_by=cls.user,
        )
        cls.events = [
            EventFactory.create(
                name="test",
                description="description1",
                start_date="2025-01-01",
                end_date="2025-01-02",
            ),
            EventFactory.create(
                name="hello",
                description="description2",
                start_date="2025-01-03",
                end_date="2025-01-04",
            ),
        ]

    def test_report_query(self):
        def _query():
            return self.query_check(
                self.Query.EVENTS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        content = _query()
        assert content["data"]["events"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    dict(
                        id=self.gID(event.id),
                        name=event.name,
                        description=event.description,
                        startDate=str(event.start_date),
                        endDate=str(event.end_date),
                        location=event.location,
                    )
                    for event in self.events
                ],
            ),
        }, content


class TestYouTubeVideoQuery(TestCase):
    class Query:
        YOUTUBE_VIDEOS = """
          query youtubeVideos($pagination: OffsetPaginationInput,$order: YouTubeVideoOrder) {
            youtubeVideos(pagination: $pagination,order:$order) {
              totalCount
              results {
                id
                videoUrl
                title
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
        cls.user = UserFactory.create(email="user22@gmail.com")

    def test_youtube_videos_query(self):
        def _query():
            return self.query_check(
                self.Query.YOUTUBE_VIDEOS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        self.force_login(self.user)
        # Create videos after login
        videos = [
            YouTubeVideoFactory.create(
                title="Video One",
                video_url="https://video1.com",
                release_date="2025-06-01",
            ),
            YouTubeVideoFactory.create(
                title="Video Two",
                video_url="https://video2.com",
                release_date="2025-06-01",
            ),
        ]

        content = _query()
        assert content["data"]["youtubeVideos"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    dict(
                        id=self.gID(video.id),
                        title=video.title,
                        videoUrl=video.video_url,
                    )
                    for video in videos
                ],
            ),
        }, content


class TestArtWorksQuery(TestCase):
    class Query:
        ARTWORKS = """
            query artWorks($pagination: OffsetPaginationInput, $order: ArtworkOrder) {
                artWorks(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        id
                        name
                        image {
                            url
                        }
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.artworks = [
            ArtworkFactory.create(
                name="Mona Lisa",
            ),
            ArtworkFactory.create(
                name="Starry Night",
            ),
        ]

    def test_artworks_query(self):
        def _query():
            return self.query_check(
                self.Query.ARTWORKS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        content = _query()
        assert content["data"]["artWorks"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    {
                        "id": self.gID(artwork.pk),
                        "name": artwork.name,
                        "image": {
                            "url": f"http://testserver{artwork.image.url if artwork.image else None}",
                        },
                    }
                    for artwork in self.artworks
                ],
            ),
        }, content


class TestGalleryQuery(TestCase):
    class Query:
        GALLERIES = """
            query galleries($pagination: OffsetPaginationInput, $order: GalleryOrder) {
                galleries(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        description
                        id
                        isArchived
                        name
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.galleries = [
            GalleryFactory.create(
                name="Gallery 1",
                description="Description1",
                is_archived=False,
            ),
            GalleryFactory.create(
                name="Gallery2",
                description="Description2",
                is_archived=False,
            ),
        ]

    def test_gallery_query(self):
        def _query():
            return self.query_check(
                self.Query.GALLERIES,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        content = _query()
        assert content["data"]["galleries"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    {
                        "id": self.gID(gallery.pk),
                        "name": gallery.name,
                        "description": gallery.description,
                        "isArchived": gallery.is_archived,
                    }
                    for gallery in self.galleries
                ],
            ),
        }, content


class TestGalleryItemQuery(TestCase):
    class Query:
        GALLERY_ITEMS = """
            query galleryItems($pagination: OffsetPaginationInput, $order: GalleryItemOrder) {
                galleryItems(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        limit
                        offset
                    }
                    results {
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
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.gallery = GalleryFactory.create()
        cls.gallery_items = [
            GalleryItemFactory.create(
                caption="Caption1",
                is_archived=False,
                gallery=cls.gallery,
            ),
            GalleryItemFactory.create(
                caption="Caption2",
                is_archived=False,
                gallery=cls.gallery,
            ),
        ]

    def test_gallery_items_query(self):
        def _query():
            return self.query_check(
                self.Query.GALLERY_ITEMS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        content = _query()
        assert content["data"]["galleryItems"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    {
                        "id": self.gID(item.pk),
                        "caption": item.caption,
                        "isArchived": item.is_archived,
                        "image": {
                            "url": f"http://testserver{item.image.url if item.image else None}",
                        },
                        "gallery": {"id": self.gID(item.gallery.pk)},
                    }
                    for item in self.gallery_items
                ],
            ),
        }, content


class ChangemakerQuery(TestCase):
    class Query:
        CHANGEMAKER = """
            query changemakers($pagination: OffsetPaginationInput, $order: ChangemakerOrder) {
                changemakers(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        id
                        name
                        description
                        facebookLink
                        linkdinLink
                        instagramLink
                        logo{
                            url
                        }
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="user100@gmail.com")
        cls.user_resource_kwargs = dict(
            created_by=cls.user,
            modified_by=cls.user,
        )
        cls.changemakers = [
            ChangemakerFactory.create(
                name="test1",
                description="Description 1",
                facebook_link="https//fbtest1.com",
                linkdin_link="https//lktest1.com",
                instagram_link="https//instatest1.com",
            ),
            ChangemakerFactory.create(
                name="test2",
                description="Description 2",
                facebook_link="https//fbtest2.com",
                linkdin_link="https//lntest2.com",
                instagram_link="https//instatest2.com",
            ),
        ]

    def test_changemaker_query(self):
        def _query():
            return self.query_check(
                self.Query.CHANGEMAKER,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        content = _query()
        assert content["data"]["changemakers"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    {
                        "id": self.gID(change.pk),
                        "name": change.name,
                        "description": change.description,
                        "instagramLink": change.instagram_link,
                        "linkdinLink": change.linkdin_link,
                        "facebookLink": change.facebook_link,
                        "logo": {
                            "url": f"http://testserver{change.logo.url if change.logo else None}",
                        },
                    }
                    for change in self.changemakers
                ],
            ),
        }, content
