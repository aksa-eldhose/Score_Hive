from django.core.exceptions import ObjectDoesNotExist

from scorehive_server.common import custom_errors
from team_players.models import Team, TeamPlayers


def valid_team_id(team_id):
    return isinstance(team_id, int) and team_id > 0


def valid_player_id(player_id):
    return isinstance(player_id, int) and player_id > 0


def valid_team_join_link(team_join_link):
    return team_join_link.isspace() or team_join_link == ""


def valid_tournament_id(tournament_id):
    return isinstance(tournament_id, int) and tournament_id > 0


def remove_player_from_team_validations(data):
    required_keys = ["player_ids", "team_id"]
    if set(required_keys) - set(data.keys()):
        raise CustomException(custom_errors.MISSING_REQUIRED_FIELDS)
    if not valid_team_id(data["team_id"]):
        raise CustomException(custom_errors.ERR_4015)
    if isinstance(data["player_ids"], list) and len(data["player_ids"]):
        for player_id in data["player_ids"]:
            if not valid_player_id(player_id):
                raise CustomException(custom_errors.ERR_1046)
    else:
        raise CustomException(custom_errors.ERR_1046)


class CustomException(Exception):
    def __init__(self, error):
        self.message = error["message"]
        self.error_code = error["error_code"]

    def to_dict(self):
        return {"error_code": self.error_code, "message": self.message}


ERROR_1025 = {"error_code": 1025, "message": "team_id is required"}
ERROR_4015 = {"error_code": 4015, "message": "TeamId should be a positive integer"}
ERROR_4012 = {"error_code": 4012, "message": "Team not found"}
ERROR_1027 = {"error_code": 1027, "message": "User is already member of the team"}
ERROR_1044 = {
    "error_code": 1044,
    "message": "Some other teams which the player is already member have"
    " tournaments in same date as this new team",
}
ERROR_1031 = {
    "error_code": 1031,
    "message": "player_id should be a positive integer",
}
ERROR_1045 = {"error_code": 1045, "message": "Please give a valid team join link"}


def validate_team_id(data):
    check_team_id_present(data)
    check_team_id_valid(data["team_id"])


def check_team_id_present(data):
    if "team_id" not in data:
        raise CustomException(ERROR_1025)


def check_team_id_valid(team_id):
    if not isinstance(team_id, int) or team_id <= 0:
        raise CustomException(ERROR_4015)


def check_player_id_valid(player_id):
    if not isinstance(player_id, int) or player_id <= 0:
        raise CustomException(ERROR_1031)


def check_if_team_valid(team_id):
    try:
        team = Team.objects.get(id=team_id)
        return team
    except ObjectDoesNotExist:
        raise CustomException(ERROR_4012)


def check_if_user_already_team_member(team_id, player_id):
    try:
        team_player = TeamPlayers.objects.get(
            team_id=team_id, player_id=player_id, status=1
        )
        return team_player
    except ObjectDoesNotExist:
        return None


def add_player_to_team(team, player):
    try:
        deleted_player = TeamPlayers.objects.get_deleted_row(
            team_id=team.pk, player_id=player.pk, status=0
        )
        deleted_player.status = 1
        deleted_player.save()
    except ObjectDoesNotExist:
        new_player = TeamPlayers(team_id=team, player_id=player)
        new_player.save()


def validate_link(link):
    if link.isspace() or link == "":
        raise CustomException(ERROR_1045)


def validate_req(request):
    check_team_id_valid(request.data["team_id"])
    check_player_id_valid(request.data["player_id"])
    validate_link(request.data["team_join_link"])
