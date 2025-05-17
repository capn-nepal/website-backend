from rest_framework import serializers

from apps.podcast.models import PodcastEpisode, PodcastSeason, VoxPop, VoxPopEpisode


class CreatePodcastSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastSeason
        fields = ("title", "description", "season_number")

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class UpdatePodcastSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastSeason
        fields = ("title", "description", "season_number")

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)


class CreatePodcastEpisodeSerializers(serializers.ModelSerializer):
    podcast_season = serializers.PrimaryKeyRelatedField(queryset=PodcastSeason.objects.all(), write_only=True)

    class Meta:
        model = PodcastEpisode
        fields = (
            "title",
            "release_date",
            "thumbnail",
            "video_url",
            "episode_number",
            "podcast_season",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class UpdatePodcastEpisodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = PodcastEpisode
        fields = (
            "title",
            "release_date",
            "thumbnail",
            "video_url",
            "episode_number",
            "podcast_season",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)


class CreateVoxPopSerializers(serializers.ModelSerializer):
    class Meta:
        model = VoxPop
        fields = ("title", "description", "season_number")

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["modified_by"] = self.context["request"].user
        return super().create(validated_data)


class UpdateVoxPopSerializers(serializers.ModelSerializer):
    class Meta:
        model = VoxPop
        fields = ("title", "description", "season_number")

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)


class CreateVoxPopEpisodeSerializers(serializers.ModelSerializer):
    voxpop_season = serializers.PrimaryKeyRelatedField(queryset=VoxPop.objects.all(), write_only=True)

    class Meta:
        model = VoxPopEpisode
        fields = (
            "title",
            "episode_number",
            "voxpop_season",
            "video_url",
            "thumbnail",
            "release_date",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class UpdateVoxPopEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoxPopEpisode
        fields = (
            "title",
            "episode_number",
            "voxpop_season",
            "video_url",
            "thumbnail",
            "release_date",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)
