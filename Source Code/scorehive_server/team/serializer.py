from rest_framework import serializers

from .models import City, Team


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=2, max_length=50)

    class Meta:
        model = Team
        fields = "__all__"

    def validate_logo_url(self, value):
        allowed = ["image/jpeg", "image/png"]
        if value.content_type not in allowed:
            raise serializers.ValidationError("This file type is not allowed")

        if value.size > 2 * 1024 * 1024:  # 2 MB in bytes
            raise serializers.ValidationError("File size should not exceed 2 MB.")

        return value


class CitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, min_length=2)

    class Meta:
        model = City
        fields = ("id", "name")


class TeamSerializerII(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Team
        fields = ("id", "name", "city", "logo_url")
