from rest_framework import serializers

from .models import TournamentGroups, TournamentGroupTeams


class TournamentGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=2, max_length=100)

    class Meta:
        model = TournamentGroups
        fields = "__all__"


class TournamentGroupTeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentGroupTeams
        fields = "__all__"
