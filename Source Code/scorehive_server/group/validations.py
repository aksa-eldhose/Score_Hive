from scorehive_server.common import custom_errors


def valid_tournament_id(tournament_id):
    if not isinstance(tournament_id, int) or tournament_id <= 0:
        raise CustomException(custom_errors.ERR_1038)


def valid_team_id(team_id):
    return isinstance(team_id, int) and team_id > 0


def valid_group_id(group_id):
    return isinstance(group_id, int) and group_id > 0


def validate_teams(data):
    if isinstance(data["team_ids"], list) and len(data["team_ids"]):
        for team_id in data["team_ids"]:
            if not valid_team_id(team_id):
                raise CustomException(custom_errors.ERR_1057)
    else:
        raise CustomException(custom_errors.ERR_1057)


class CustomException(Exception):
    def __init__(self, error):
        self.message = error["message"]
        self.error_code = error["error_code"]

    def to_dict(self):
        return {"error_code": self.error_code, "message": self.message}
