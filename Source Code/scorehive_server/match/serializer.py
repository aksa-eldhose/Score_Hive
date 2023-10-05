from rest_framework import serializers

from round.serializer import RoundSerializer
from team.serializer import TeamSerializerII
from tournament.serializer import CitySerializer, GroundSerializer

from .models import Matches


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matches
        fields = "__all__"


class MatchSerializerII(serializers.ModelSerializer):
    team1 = TeamSerializerII("team1", read_only=True)
    team2 = TeamSerializerII("team2", read_only=True)
    city = CitySerializer(source="city_id", read_only=True)
    ground = GroundSerializer(source="ground_id", read_only=True)
    round = RoundSerializer(source="round_id", read_only=True)

    class Meta:
        model = Matches
        fields = (
            "id",
            "tournament_id",
            "team1",
            "team2",
            "city",
            "round",
            "ground",
            "match_type",
            "date_time",
            "over_per_bowler",
            "total_overs",
            "winner_team_id",
        )
