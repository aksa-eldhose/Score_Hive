import datetime

from rest_framework import serializers

from team.serializer import CitySerializer, TeamSerializerII
from team_tournaments.models import TeamTournaments

from .models import Ground, Tournament

date_format = "%Y-%m-%d"


class TournamentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=2, max_length=100)
    ball_type = serializers.IntegerField(validators=[lambda x: x != ""])
    match_type = serializers.IntegerField(validators=[lambda x: x != ""])
    tournament_type = serializers.IntegerField(validators=[lambda x: x != ""])

    class Meta:
        model = Tournament
        fields = "__all__"

    def validate_logo_url(self, value):
        allowed = ["image/jpeg", "image/png"]
        if value.content_type not in allowed:
            raise serializers.ValidationError("This file type is not allowed")
        return value

    def validate_banner_url(self, value):
        allowed_format = ["image/jpeg", "image/png"]
        if value.content_type not in allowed_format:
            raise serializers.ValidationError("This file type is not allowed")
        return value

    def validate_start_date(self, value):
        tournament = self.context.get("tournament", None)
        if not tournament:
            date1 = value
            today = datetime.date.today()
            if date1 < today:
                raise serializers.ValidationError(
                    "This start_date should be greater than or equal to current date"
                )
            try:
                datetime.datetime.strptime(value.strftime(date_format), date_format)
                return value
            except Exception:
                raise serializers.ValidationError("This start_date is not valid")
        else:
            if tournament.start_date <= datetime.date.today():
                return value
            else:
                if value < datetime.date.today():
                    raise serializers.ValidationError(
                        "This start_date should be greater than or equal to current date"
                    )
                else:
                    return value

    def validate_end_date(self, value):
        date1 = value
        today = datetime.date.today()
        if not self.context.get("tournament", None):
            check_date = self.initial_data.get("start_date")
            if (
                self.initial_data.get("start_date") is None
                or self.initial_data.get("start_date") == ""
            ):
                return
        else:
            check_date = self.initial_data.get(
                "start_date", str(self.context.get("tournament").start_date)
            )
            if (
                self.initial_data.get("start_date") is None
                or self.initial_data.get("start_date") == ""
            ):
                return

        try:
            start_date = datetime.datetime.strptime(check_date, date_format).date()
            if date1 < today:
                raise serializers.ValidationError(
                    "This end_date should be greater than or equal to current date"
                )
            if date1 < start_date:
                raise serializers.ValidationError(
                    "This end_date should be greater than or equal to start date"
                )
            return value
        except ValueError:
            pass


class GroundSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=2, max_length=100)

    class Meta:
        model = Ground
        fields = ("id", "name")


class TournamentSerializerII(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    ground = GroundSerializer(read_only=True)

    class Meta:
        model = Tournament
        fields = "__all__"


class TeamTournamentSerializerII(serializers.ModelSerializer):
    team_id = TeamSerializerII()

    class Meta:
        model = TeamTournaments
        fields = ["team_id"]


class HomeTournamentSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    ground = GroundSerializer(read_only=True)
    tournament_status = serializers.SerializerMethodField()

    def get_tournament_status(self, data):
        today = datetime.date.today()
        if data.end_date < today:
            return 0
        elif data.start_date <= today <= data.end_date:
            return 1
        else:
            return 2

    class Meta:
        model = Tournament
        fields = "__all__"
