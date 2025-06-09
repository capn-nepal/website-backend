from apps.podcast.factories import (
    PodcastEpisodeFactory,
    PodcastSeasonFactory,
    VoxPopEpisodeFactory,
    VoxPopFactory,
)
from apps.user.factories import UserFactory
from main.tests.base_test import TestCase


class TestPodcastSeasonQuery(TestCase):
    class Query:
        PODCAST_SEASONS = """
            query podcastSeasons($pagination: OffsetPaginationInput, $order: PodcastSeasonOrder) {
                podcastSeasons(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        id
                        title
                        description
                        seasonNumber
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="user1@gmail.com")
        cls.seasons = [
            PodcastSeasonFactory.create(
                title="Season 1",
                description="First season",
                season_number=1,
            ),
            PodcastSeasonFactory.create(
                title="Season 2",
                description="Second season",
                season_number=2,
            ),
        ]

    def test_podcast_season_query(self):
        def _query():
            return self.query_check(
                self.Query.PODCAST_SEASONS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        # Without authentication
        content = _query()
        assert content["data"]["podcastSeasons"]["totalCount"] == 0

        # With authentication
        self.force_login(self.user)
        content = _query()
        assert content["data"]["podcastSeasons"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    dict(
                        id=self.gID(season.pk),
                        title=season.title,
                        description=season.description,
                        seasonNumber=season.season_number,
                    )
                    for season in self.seasons
                ],
            ),
        }, content


class TestPodcastEpisodeQuery(TestCase):
    class Query:
        PODCAST_EPISODES = """
            query podcastEpisodes($pagination: OffsetPaginationInput, $order: PodcastEpisodeOrder) {
                podcastEpisodes(pagination: $pagination, order: $order) {
                    totalCount
                    pageInfo {
                        offset
                        limit
                    }
                    results {
                        id
                        title
                        episodeNumber
                        videoUrl
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="user1@gmail.com")
        cls.pod_cast_season1 = PodcastSeasonFactory.create(
            title="Season 11",
            description="nothing season",
            season_number=11,
        )

        cls.episodes = [
            PodcastEpisodeFactory.create(
                title="Episode 1",
                episode_number=1,
                video_url="https://example.com/ep1",
                podcast_season=cls.pod_cast_season1,
                release_date="2025-01-11",
            ),
            PodcastEpisodeFactory.create(
                title="Episode 2",
                episode_number=2,
                video_url="https://example.com/ep2",
                podcast_season=cls.pod_cast_season1,
                release_date="2025-01-11",
            ),
        ]

    def test_podcast_episode_query(self):
        def _query():
            return self.query_check(
                self.Query.PODCAST_EPISODES,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        # Without login
        content = _query()
        assert content["data"]["podcastEpisodes"]["totalCount"] == 0

        # With login
        self.force_login(self.user)
        content = _query()
        assert content["data"]["podcastEpisodes"] == {
            **self.g_pagination(
                offset=0,
                limit=10,
                total_count=2,
                results=[
                    dict(
                        id=self.gID(episode.pk),
                        title=episode.title,
                        episodeNumber=episode.episode_number,
                        videoUrl=episode.video_url,
                    )
                    for episode in self.episodes
                ],
            ),
        }, content


class TestVoxPopSeasonQuery(TestCase):
    class Query:
        VOXPOP_SEASONS = """
            query voxpopSeasons($pagination: OffsetPaginationInput, $order: VoxPopOrder) {
                voxpopSeasons(pagination: $pagination, order: $order) {
                    pageInfo {
                        limit
                        offset
                    }
                    totalCount
                    results {
                        id
                        title
                        description
                        seasonNumber
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="user1@gmail.com")
        cls.seasons = [
            VoxPopFactory.create(
                title="Season A",
                description="Voxpop First",
                season_number=1,
            ),
            VoxPopFactory.create(
                title="Season B",
                description="Voxpop Second",
                season_number=2,
            ),
        ]

    def test_voxpop_season_query(self):
        def _query():
            return self.query_check(
                self.Query.VOXPOP_SEASONS,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        # Without login
        content = _query()
        assert content["data"]["voxpopSeasons"]["totalCount"] == 0

        # With login
        self.force_login(self.user)
        content = _query()
        assert content["data"]["voxpopSeasons"] == {
            "pageInfo": {"limit": 10, "offset": 0},
            "totalCount": 2,
            "results": [
                dict(
                    id=self.gID(season.pk),
                    title=season.title,
                    description=season.description,
                    seasonNumber=season.season_number,
                )
                for season in self.seasons
            ],
        }, content


class TestVoxPopEpisodeQuery(TestCase):
    class Query:
        VOXPOP_EPISODES = """
            query voxpopEpisodes($pagination: OffsetPaginationInput, $order: VoxPopEpisodeOrder) {
                voxpopEpisodes(pagination: $pagination, order: $order) {
                    pageInfo {
                        limit
                        offset
                    }
                    totalCount
                    results {
                        id
                        title
                        episodeNumber
                        videoUrl
                        voxpopSeason {
                            pk
                        }
                    }
                }
            }
        """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create(email="user1@gmail.com")
        cls.season = VoxPopFactory.create(title="Season X", season_number=101)
        cls.episodes = [
            VoxPopEpisodeFactory.create(
                title="Voxpop Ep1",
                release_date="2025-02-01",
                video_url="https://example.com/vx1",
                voxpop_season=cls.season,
                episode_number=1,
            ),
            VoxPopEpisodeFactory.create(
                title="Voxpop Ep2",
                episode_number=2,
                release_date="2025-02-02",
                video_url="https://example.com/vx2",
                voxpop_season=cls.season,
            ),
        ]

    def test_voxpop_episode_query(self):
        def _query():
            return self.query_check(
                self.Query.VOXPOP_EPISODES,
                variables={
                    "pagination": {"limit": 10, "offset": 0},
                    "order": {"id": "ASC"},
                },
            )

        # Without login
        content = _query()
        assert content["data"]["voxpopEpisodes"]["totalCount"] == 0

        # With login
        self.force_login(self.user)
        content = _query()
        assert content["data"]["voxpopEpisodes"] == {
            "pageInfo": {"limit": 10, "offset": 0},
            "totalCount": 2,
            "results": [
                dict(
                    id=self.gID(episode.pk),
                    title=episode.title,
                    episodeNumber=episode.episode_number,
                    videoUrl=episode.video_url,
                    voxpopSeason={"pk": str(episode.voxpop_season.pk)},
                )
                for episode in self.episodes
            ],
        }, content
