from rest_framework import serializers

from apps.common.models import (
    Event,
    EventAsset,
    GalleryItem,
    Report,
    YouTubeVideo,
)


class UserResourceSerializer(serializers.ModelSerializer):
    modified_at = serializers.DateTimeField(read_only=True)
    modified_by = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        if "created_by" in self.Meta.model._meta._forward_fields_map:  # type: ignore[reportAttributeAccessIssue]
            validated_data["created_by"] = self.context["request"].user
        if "modified_by" in self.Meta.model._meta._forward_fields_map:  # type: ignore[reportAttributeAccessIssue]
            validated_data["modified_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "modified_by" in self.Meta.model._meta._forward_fields_map:  # type: ignore[reportAttributeAccessIssue]
            validated_data["modified_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "name",
            "description",
            "location",
            "start_date",
            "end_date",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class UpdateEventSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = Event
        fields = (
            "name",
            "description",
            "location",
            "start_date",
            "end_date",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)


class EventAssetsSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True)

    class Meta:
        model = EventAsset
        fields = ("event", "image")

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class CreateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ("title", "description", "published_date", "report_file", "status")

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["modified_by"] = self.context["request"].user
        return super().create(validated_data)


class UpdateReportSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = Report
        fields = ("title", "description", "published_date", "report_file", "status")

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)


class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = ("image", "image_type")

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class CreateYoutubeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = (
            "title",
            "video_url",
            "thumbnail",
            "release_date",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class UpdateYoutubeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = (
            "title",
            "video_url",
            "thumbnail",
            "release_date",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)
