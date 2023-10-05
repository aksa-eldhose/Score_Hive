import datetime

from django.core.exceptions import ObjectDoesNotExist

from round.models import TournamentRounds
from scorehive_server.common import custom_errors
from team.models import Team
from team_tournaments.models import TeamTournaments
from tournament.models import Tournament


def valid_tournament_id(tournament_id, user):
    if isinstance(tournament_id, int) and tournament_id > 0:
        try:
            tournament = Tournament.objects.get(id=tournament_id, user=user, status=1)
            if tournament.end_date < datetime.date.today():
                raise CustomException(custom_errors.ERR_1079)
        except ObjectDoesNotExist:
            raise CustomException(custom_errors.ERR_1039)
    else:
        raise CustomException(custom_errors.ERR_1038)


def validate_match_id(match_id):
    if not isinstance(match_id, int) and match_id > 0:
        raise CustomException(custom_errors.ERR_1067)


def validate_team(team, tournament):
    if isinstance(team, int) and team > 0:
        try:
            team_id = Team.objects.get(id=team, status=0).id
            TeamTournaments.objects.get(
                team_id=team_id, tournament_id=tournament, status=1
            )
        except ObjectDoesNotExist:
            raise CustomException(custom_errors.ERR_1078)
    else:
        raise CustomException(custom_errors.ERR_4015)


def validate_match_type(match_type):
    if not isinstance(match_type, int) and match_type in [1, 0]:
        raise CustomException(custom_errors.ERR_1080)


def validate_round(round_id, tournament_id):
    if isinstance(round_id, int) and round_id > 0:
        try:
            TournamentRounds.objects.get(
                round_id=round_id,
                tournament_id=tournament_id,
                status=1,
                round_id__status=1,
            )
        except ObjectDoesNotExist:
            raise CustomException(custom_errors.ERR_4016)
    else:
        raise CustomException(custom_errors.ERR_4017)


def validate_over(over, over_per_bowler):
    if isinstance(over, int) and over > 0:
        if isinstance(over_per_bowler, int) and over_per_bowler > 0:
            if over_per_bowler > over:
                raise CustomException(custom_errors.ERR_1081)
        else:
            raise CustomException(custom_errors.ERR_1082)
    else:
        raise CustomException(custom_errors.ERR_1083)


def validate_date_time(date_time, tournament_id):
    date_time = datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
    if date_time < datetime.datetime.now():
        raise CustomException(custom_errors.ERR_1086)
    tournament = Tournament.objects.get(id=tournament_id)
    if date_time.date() > tournament.end_date:
        raise CustomException(custom_errors.ERR_1087)


def validate_request(request):
    if request.data["tournament_id"]:
        valid_tournament_id(request.data["tournament_id"], request.user.id)
    if request.data["team1"]:
        validate_team(request.data["team1"], request.data["tournament_id"])
    if request.data["team2"]:
        validate_team(request.data["team2"], request.data["tournament_id"])
    if request.data["match_type"]:
        validate_match_type(request.data["match_type"])
    if request.data["round_id"]:
        validate_round(request.data["round_id"], request.data["tournament_id"])
    if request.data["match_type"] == "0":
        validate_over(
            request.data["total_overs"],
            request.data["over_per_bowler"],
        )
    if request.data["date_time"]:
        validate_date_time(request.data["date_time"], request.data["tournament_id"])


class CustomException(Exception):
    def __init__(self, error):
        self.message = error["message"]
        self.error_code = error["error_code"]

    def to_dict(self):
        return {"error_code": self.error_code, "message": self.message}
