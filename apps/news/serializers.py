from rest_framework import serializers

from apps.news.models import News


class CreateNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            "title",
            "description",
            "published_date",
            "news_type",
            "cover_image",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class UpdateNewsSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = News
        fields = (
            "title",
            "description",
            "published_date",
            "status",
            "news_type",
            "cover_image",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)
