from rest_framework import serializers

from apps.blog.models import Blog, BlogAsset


class CreateBlogSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        # Set the logged-in user as the author
        validated_data["author"] = user
        return super().create(validated_data)

    class Meta:
        model = Blog
        fields = (
            "title",
            "published_date",
            "description",
            "cover_image",
            "featured",
            "content",
        )


class UpdateBlogSerializers(serializers.ModelSerializer):
    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = Blog
        fields = (
            "title",
            "published_date",
            "description",
            "cover_image",
            "featured",
            "content",
        )


class CreateBlogAssetSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["modified_by"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        model = BlogAsset
        fields = ("blog", "file")
