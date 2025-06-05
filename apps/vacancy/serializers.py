from rest_framework import serializers

from .models import JobVacancy, Position


class CreatePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = (
            "name",
            "summary",
            "key_responsibilities",
            "qualifications",
            "preferred_skills",
            "employment_type",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class UpdatePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = (
            "name",
            "summary",
            "key_responsibilities",
            "qualifications",
            "preferred_skills",
            "employment_type",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)


class CreateJobVacancySerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), write_only=True)

    class Meta:
        model = JobVacancy
        fields = (
            "position",
            "description",
            "number_of_vacancies",
            "deadline",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["modified_by"] = user
        return super().create(validated_data)


class UpdateJobVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobVacancy
        fields = (
            "position",
            "description",
            "number_of_vacancies",
            "deadline",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user
        validated_data["modified_by"] = user
        return super().update(instance, validated_data)
