import typing

from django.contrib.auth import authenticate
from django.utils.translation import gettext
from rest_framework import serializers

from .validators import CustomMaximumLengthValidator


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_password(self, password):
        # this will now only handle max-length in the login
        CustomMaximumLengthValidator().validate(password=password)
        return password

    @typing.override
    def validate(self, attrs):
        # NOTE: authenticate only works for active users
        authenticate_user = authenticate(
            email=attrs["email"].lower(),
            password=attrs["password"],
        )
        if authenticate_user is None:
            raise serializers.ValidationError("No active account found with the given credentials")
        return {"user": authenticate_user}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, password):
        user = self.context["request"].user
        if not user.check_password(password):
            raise serializers.ValidationError(gettext("Invalid old Password"))
        return password

    def validate(self, attrs):
        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError(gettext("New and old provided passwords are same"))
        return attrs

    def validate_new_password(self, password):
        CustomMaximumLengthValidator().validate(password=password)
        return password

    def save(self, **_):
        assert isinstance(self.validated_data, dict)
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save(update_fields=("password",))
