from apps.podcast.factories import (
    PodcastEpisodeFactory,
    PodcastSeasonFactory,
    VoxPopEpisodeFactory,
    VoxPopFactory,
)
from apps.user.factories import UserFactory
from main.tests.base_test import TestCase


class TestPodcastSeasonMutation(TestCase):
    class Mutation:
        CREATE_PODCAST_SEASON = """
          mutation CreatePodcastSeason($data: CreatePodcastSeasonInput!) {
            createPodcastSeason(data: $data) {
              ... on PodcastSeasonTypeMutationResponseType {
                errors
                ok
                result {
                  id
                  title
                  description
                  seasonNumber
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
        UPDATE_PODCAST_SEASON = """
          mutation UpdatePodcastSeason($pk: ID!, $data: UpdatePodcastSeasonInput!) {
            updatePodcastSeason(pk: $pk, data: $data) {
              ... on PodcastSeasonTypeMutationResponseType {
                errors
                result {
                  id
                  title
                  description
                  seasonNumber
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
        cls.user = UserFactory.create(email="testuser@example.com")

    def _create_season_mutation(self, season_data: dict, **kwargs):
        return self.query_check(
            self.Mutation.CREATE_PODCAST_SEASON,
            variables={"data": season_data},
            **kwargs,
        )

    def _update_season_mutation(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_PODCAST_SEASON,
            variables={
                "pk": pk,
                "data": data,
            },
        )

    def test_create_podcast_season(self):
        season_data = {
            "title": "Season 1",
            "description": "The first season",
            "seasonNumber": 1,
        }

        # Without authentication
        content = self._create_season_mutation(season_data)
        assert content["data"]["createPodcastSeason"]["messages"] == [
            {
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_season_mutation(season_data)
        response_data = content["data"]["createPodcastSeason"]

        assert response_data["errors"] is None, content
        assert response_data["ok"] is True
        assert response_data["result"]["title"] == "Season 1"
        assert response_data["result"]["description"] == "The first season"
        assert response_data["result"]["seasonNumber"] == 1

    def test_update_podcast_season(self):
        season = PodcastSeasonFactory.create(
            title="Old Title",
            description="Old description",
            season_number=1,
        )

        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "seasonNumber": 1,
        }

        # Without authentication
        content = self._update_season_mutation(self.gID(season.pk), update_data)
        assert content["data"]["updatePodcastSeason"]["messages"] == [
            {
                "message": "User is not authenticated.",
            },
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._update_season_mutation(self.gID(season.pk), update_data)
        response_data = content["data"]["updatePodcastSeason"]

        assert response_data["errors"] is None, content
        assert response_data["result"] == {
            "id": self.gID(season.pk),
            "title": "Updated Title",
            "description": "Updated description",
            "seasonNumber": 1,
        }, content

        season.refresh_from_db()
        assert season.title == "Updated Title"
        assert season.description == "Updated description"
        assert season.season_number == 1


class TestVoxPopSeasonMutation(TestCase):
    class Mutation:
        CREATE_VOXPOP_SEASON = """
          mutation CreateVoxpopSeason($data: CreateVoxPopSeasonInput!) {
            createVoxpopSeason(data: $data) {
              ... on VoxPopSeasonTypeMutationResponseType {
                errors
                result {
                  id
                  title
                  description
                  seasonNumber
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

        UPDATE_VOXPOP_SEASON = """
          mutation UpdateVoxpopSeason($pk: ID!, $data: UpdateVoxPopSeasonInput!) {
            updateVoxpopSeason(pk: $pk, data: $data) {
              ... on VoxPopSeasonTypeMutationResponseType {
                errors
                result {
                  id
                  title
                  description
                  seasonNumber
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
        cls.user = UserFactory.create(email="testuser@example.com")

    def _create_voxpop_season(self, season_data: dict, **kwargs):
        return self.query_check(
            self.Mutation.CREATE_VOXPOP_SEASON,
            variables={"data": season_data},
            **kwargs,
        )

    def _update_voxpop_season(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_VOXPOP_SEASON,
            variables={"pk": pk, "data": data},
        )

    def test_create_voxpop_season(self):
        season_data = {
            "title": "Voxpop Season 1",
            "seasonNumber": 1,
        }

        # Without authentication
        content = self._create_voxpop_season(season_data)
        assert content["data"]["createVoxpopSeason"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._create_voxpop_season(season_data)
        response_data = content["data"]["createVoxpopSeason"]

        assert response_data["errors"] is None, content
        assert response_data["result"]["title"] == "Voxpop Season 1"
        assert response_data["result"]["seasonNumber"] == 1

    def test_update_voxpop_season(self):
        season = VoxPopFactory.create(
            title="Old Voxpop Title",
            description="Old Description",
            season_number=1,
        )

        update_data = {
            "title": "New Voxpop Title",
            "description": "New Description",
            "seasonNumber": 1,
        }

        # Without authentication
        content = self._update_voxpop_season(self.gID(season.pk), update_data)
        assert content["data"]["updateVoxpopSeason"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._update_voxpop_season(self.gID(season.pk), update_data)
        response_data = content["data"]["updateVoxpopSeason"]

        assert response_data["errors"] is None, content
        assert response_data["result"] == {
            "id": self.gID(season.pk),
            "title": "New Voxpop Title",
            "description": "New Description",
            "seasonNumber": 1,
        }

        season.refresh_from_db()
        assert season.title == "New Voxpop Title"


class TestPodcastEpisodeMutation(TestCase):
    class Mutation:
        CREATE_PODCAST_EPISODE = """
          mutation CreatePodcastEpisode($data: CreatePodcastEpisodeInput!) {
            createPodcastEpisode(data: $data) {
              ... on PodcastEpisodeTypeMutationResponseType {
                errors
                result {
                  id
                  title
                  episodeNumber
                  videoUrl
                  releaseDate
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
        UPDATE_PODCAST_EPISODE = """
          mutation UpdatePodcastEpisode($pk: ID!, $data: UpdatePodcastEpisodeInput!) {
            updatePodcastEpisode(pk: $pk, data: $data) {
              ... on PodcastEpisodeTypeMutationResponseType {
                errors
                ok
                result {
                  id
                  title
                  videoUrl
                  releaseDate
                  episodeNumber
                  isArchived
                  podcastSeason {
                    pk
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
        ARCHIVE_PODCAST_EPISODE = """
          mutation ArchivePodcastEpisode($pk: ID!) {
            archivePodcastEpisode(pk: $pk) {
              ... on PodcastEpisodeTypeMutationResponseType {
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
        cls.user = UserFactory.create(email="testuserpodcastepisode@example.com")

    def _create_episode(self, data: dict, **kwargs):
        return self.query_check(
            self.Mutation.CREATE_PODCAST_EPISODE,
            variables={"data": data},
            **kwargs,
        )

    def _update_episode(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_PODCAST_EPISODE,
            variables={"pk": pk, "data": data},
        )

    def _archive_episode(self, pk):
        return self.query_check(
            self.Mutation.ARCHIVE_PODCAST_EPISODE,
            variables={"pk": pk},
        )

    def test_update_podcast_episode(self):
        season = PodcastSeasonFactory.create(season_number=122)
        episode = PodcastEpisodeFactory.create(
            title="Old Episode",
            podcast_season=season,
            episode_number=1,
            video_url="https://example.com/old",
            release_date="2025-06-01",
            is_archived=False,
        )

        update_data = {
            "title": "Updated Episode",
            "podcastSeason": self.gID(season.pk),
            "episodeNumber": 1,
            "videoUrl": "https://example.com/updated",
            "releaseDate": "2025-08-01",
        }

        # Without authentication
        content = self._update_episode(self.gID(episode.pk), update_data)
        assert content["data"]["updatePodcastEpisode"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._update_episode(self.gID(episode.pk), update_data)
        response = content["data"]["updatePodcastEpisode"]

        assert response["errors"] is None, content
        assert response["ok"] is True
        assert response["result"]["title"] == "Updated Episode"
        assert response["result"]["videoUrl"] == "https://example.com/updated"
        assert response["result"]["episodeNumber"] == 1
        assert response["result"]["isArchived"] is False
        assert response["result"]["podcastSeason"]["pk"] == str(season.pk)

    def test_archive_podcast_episode(self):
        season = PodcastSeasonFactory.create(season_number=123)
        episode = PodcastEpisodeFactory.create(
            is_archived=False,
            episode_number=1,
            podcast_season=season,
            video_url="https://example2.com/old",
            release_date="2025-06-01",
        )

        # Without authentication
        content = self._archive_episode(self.gID(episode.pk))
        assert content["data"]["archivePodcastEpisode"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With authentication
        self.force_login(self.user)
        content = self._archive_episode(self.gID(episode.pk))
        response = content["data"]["archivePodcastEpisode"]

        assert response["errors"] is None, content
        episode.refresh_from_db()
        assert episode.is_archived is True


class TestVoxPopEpisodeMutation(TestCase):
    class Mutation:
        CREATE_VOXPOP_EPISODE = """
        mutation CreateVoxpopEpisode($data: CreateVoxPopEpisodeInput!) {
          createVoxpopEpisode(data: $data) {
            ... on VoxPopEpisodeTypeMutationResponseType {
              errors
              result {
                id
                title
                videoUrl
                releaseDate
                isArchived
                episodeNumber
                voxpopSeason {
                  pk
                }
                thumbnail {
                    name
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
        UPDATE_VOXPOP_EPISODE = """
        mutation UpdateVoxpopEpisode($pk: ID!, $data: UpdateVoxPopEpisodeInput!) {
          updateVoxpopEpisode(pk: $pk, data: $data) {
            ... on VoxPopEpisodeTypeMutationResponseType {
              errors
              result {
                id
                title
                videoUrl
                releaseDate
                isArchived
                episodeNumber
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
        ARCHIVE_VOXPOP_EPISODE = """
        mutation ArchiveVoxpopEpisode($pk: ID!) {
          archiveVoxpopEpisode(pk: $pk) {
            ... on VoxPopEpisodeTypeMutationResponseType {
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
        cls.user = UserFactory.create(email="voxpopuser@example.com")

    def _update_episode(self, pk, data):
        return self.query_check(
            self.Mutation.UPDATE_VOXPOP_EPISODE,
            variables={"pk": pk, "data": data},
        )

    def _archive_episode(self, pk):
        return self.query_check(
            self.Mutation.ARCHIVE_VOXPOP_EPISODE,
            variables={"pk": pk},
        )

    def test_update_voxpop_episode(self):
        season = VoxPopFactory.create(season_number=33)
        episode = VoxPopEpisodeFactory.create(
            title="Old Vox",
            voxpop_season=season,
            episode_number=1,
            video_url="https://voxpop.com/old.mp4",
            release_date="2025-05-01",
        )

        update_data = {
            "title": "Updated Vox",
            "voxpopSeason": self.gID(season.pk),
            "episodeNumber": 1,
            "videoUrl": "https://voxpop.com/new.mp4",
            "releaseDate": "2025-08-01",
        }

        # Without login
        content = self._update_episode(self.gID(episode.pk), update_data)
        assert content["data"]["updateVoxpopEpisode"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With login
        self.force_login(self.user)
        content = self._update_episode(self.gID(episode.pk), update_data)
        result = content["data"]["updateVoxpopEpisode"]["result"]

        assert content["data"]["updateVoxpopEpisode"]["errors"] is None, content
        assert result["title"] == "Updated Vox"
        assert result["videoUrl"] == "https://voxpop.com/new.mp4"
        assert result["episodeNumber"] == 1
        assert result["isArchived"] is False

    def test_archive_voxpop_episode(self):
        season = VoxPopFactory.create(season_number=44)
        episode = VoxPopEpisodeFactory.create(
            title="Vox",
            voxpop_season=season,
            episode_number=1,
            video_url="https://voxpop.com/old.mp4",
            release_date="2025-05-01",
        )
        # Without login
        content = self._archive_episode(self.gID(episode.pk))
        assert content["data"]["archiveVoxpopEpisode"]["messages"] == [
            {"message": "User is not authenticated."},
        ], content

        # With login
        self.force_login(self.user)
        content = self._archive_episode(self.gID(episode.pk))

        assert content["data"]["archiveVoxpopEpisode"]["errors"] is None, content

        episode.refresh_from_db()
        assert episode.is_archived is True
