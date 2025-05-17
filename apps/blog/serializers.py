from rest_framework import serializers

from apps.blog.models import Author, Blog, BlogAsset


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("name", "image")


class CreateBlogSerializers(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True)

    class Meta:
        model = Blog
        fields = (
            "title",
            "published_date",
            "description",
            "cover_image",
            "featured",
            "content",
            "author",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


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
            "status",
        )


class CreateBlogAssetSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["modified_by"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        model = BlogAsset
        fields = ("blog", "file")
