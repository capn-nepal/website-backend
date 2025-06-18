from apps.common.factories import (
    EventFactory,
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

        # Without authentication
        content = _query()
        assert content["data"]["reports"]["totalCount"] == 0
        #  With authentication
        self.force_login(self.user)
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

        # Without authentication
        content = _query()
        assert content["data"]["events"]["totalCount"] == 0
        #  With authentication
        self.force_login(self.user)
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

        # Without authentication
        content = _query()
        assert content["data"]["youtubeVideos"]["totalCount"] == 0

        # With authentication
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
