from match.models import Matches
from scorehive_server.common import custom_errors
from team_players.models import TeamPlayers


def validate_match_id(match_id):
    try:
        if not isinstance(match_id, int) or match_id <= 0:
            raise CustomException(custom_errors.ERR_1067)
    except ValueError:
        raise CustomException(custom_errors.ERR_1067)


def validate_inning(inning):
    try:
        if not isinstance(inning, int) or inning <= 0:
            raise CustomException(custom_errors.ERR_1068)
    except ValueError:
        raise CustomException(custom_errors.ERR_1068)


def validate_batting_team(team_id, match_id):
    try:
        if not isinstance(team_id, int) or team_id <= 0:
            raise CustomException(custom_errors.ERR_4015)
        team1 = Matches.objects.get(id=match_id, status=1).team1
        team2 = Matches.objects.get(id=match_id, status=1).team2
        teams = [team1.id, team2.id]
        if team_id not in teams:
            raise CustomException(custom_errors.ERR_1090)
    except ValueError:
        raise CustomException(custom_errors.ERR_4015)


def validate_over(over):
    try:
        if not isinstance(over, int) or over <= 0:
            raise CustomException(custom_errors.ERR_1069)
    except ValueError:
        raise CustomException(custom_errors.ERR_1069)


def validate_ball_number(ball_number):
    try:
        if not isinstance(ball_number, int) or ball_number <= 0:
            raise CustomException(custom_errors.ERR_1070)
    except ValueError:
        raise CustomException(custom_errors.ERR_1070)


def validate_striker_id(striker_id, team):
    try:
        if not isinstance(striker_id, int) or striker_id <= 0:
            raise CustomException(custom_errors.ERR_1071)
        else:
            players = TeamPlayers.objects.filter(team_id=team, status=1).values_list(
                "player_id", flat=True
            )
            if striker_id not in players:
                raise CustomException(custom_errors.ERR_1072)
    except ValueError:
        raise CustomException(custom_errors.ERR_1071)


def validate_non_striker_id(non_striker_id, team):
    try:
        if not isinstance(non_striker_id, int) or non_striker_id <= 0:
            raise CustomException(custom_errors.ERR_1073)
        else:
            players = TeamPlayers.objects.filter(team_id=team, status=1).values_list(
                "player_id", flat=True
            )
            if non_striker_id not in players:
                raise CustomException(custom_errors.ERR_1089)
    except ValueError:
        raise CustomException(custom_errors.ERR_1071)


def validate_bowler_id(bowler_id, match_id, batting_team):
    try:
        if not isinstance(bowler_id, int) or bowler_id <= 0:
            raise CustomException(custom_errors.ERR_1074)
        else:
            team1 = Matches.objects.get(id=match_id, status=1).team1
            team2 = Matches.objects.get(id=match_id, status=1).team2
            team = {team1, team2} - {batting_team}
            players = TeamPlayers.objects.filter(
                team_id__in=team, status=1
            ).values_list("player_id", flat=True)
            if bowler_id not in players:
                raise CustomException(custom_errors.ERR_1091)
    except ValueError:
        raise CustomException(custom_errors.ERR_1071)


def validate_runs(runs):
    if not isinstance(runs, int) or runs < 0:
        raise CustomException(custom_errors.ERR_1075)


def validate_extras(extras):
    choices = [0, 1, 2]
    if extras not in choices:
        raise CustomException(custom_errors.ERR_1092)


def validate_request(data):
    required_keys = [
        "match_id",
        "inning",
        "batting_team",
        "striker_id",
        "runs",
        "ball_number",
        "over",
    ]

    for entry in data:
        missing_keys = set(required_keys) - set(entry.keys())
        if missing_keys:
            raise CustomException(custom_errors.MISSING_REQUIRED_FIELDS)
        validate_match_id(entry["match_id"])
        validate_inning(entry["inning"])
        validate_batting_team(entry["batting_team"], entry["match_id"])
        validate_over(entry["over"])
        validate_ball_number(entry["ball_number"])
        validate_striker_id(entry["striker_id"], entry["batting_team"])
        validate_bowler_id(entry["bowler_id"], entry["match_id"], entry["batting_team"])
        validate_runs(entry["runs"])

        try:
            if entry["striker_id"] == entry["non_striker_id"]:
                raise CustomException(custom_errors.ERR_1093)
            validate_non_striker_id(entry["non_striker_id"], entry["batting_team"])
            validate_extras(entry["extras"])
        except KeyError:
            pass


class CustomException(Exception):
    def __init__(self, error):
        self.message = error["message"]
        self.error_code = error["error_code"]

    def to_dict(self):
        return {"error_code": self.error_code, "message": self.message}
