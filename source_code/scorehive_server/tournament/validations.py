from scorehive_server.common import custom_errors
from team.models import City
from team_players import validations
from team_players.validations import \
    CustomException as DeleteTournamentCustomException

from .models import Ground


class TournamentValidation:
    def validate_tour_data(self, data):
        allowed_fields = [
            "logo_url",
            "banner_url",
            "match_type",
            "ball_type",
            "name",
            "tournament_type",
            "start_date",
            "end_date",
            "description",
            "city",
            "ground",
        ]
        for fields in data:
            if fields not in allowed_fields:
                raise CustomException("unknown field found", 5001)
        if "ball_type" in data:
            self.validate_ball_type(data)
        if "tournament_type" in data:
            self.validate_tournament_type(data)
        if "match_type" in data:
            self.validate_match_type(data)
        if "description" in data:
            self.validate_description(data)
        if "logo_url" in data:
            logo_file = data["logo_url"]
            self.validate_logo_url(logo_file)
        if "banner_url" in data:
            banner_file = data["banner_url"]
            self.validate_banner_url(banner_file)

    def validate_query_param(self, request):
        if request.query_params:
            if len(request.query_params) == 1 and "page" in request.query_params:
                return
            else:
                raise CustomException(
                    "Invalid query parameter. Only 'page' is allowed.", 4011
                )

    def tour_id_param(self, request):
        if "id" not in request.query_params or not request.query_params["id"]:
            raise CustomException("query param id is required with a value", 4008)
        elif not request.query_params.get("id").isdigit():
            raise CustomException("query param id must be an integer", 4009)

    def validate_ball_type(self, data):
        if len(data.get("ball_type")) == 0:
            raise CustomException("ball_type cannot be blank", 5013)
        if data.get("ball_type").isdigit():
            if not 0 <= int(data.get("ball_type")) <= 2:
                raise CustomException("invalid value for ball type", 5004)
        else:
            raise CustomException("ball_type must be an Integer", 5005)

    def validate_tournament_type(self, data):
        if len(data.get("tournament_type")) == 0:
            raise CustomException("tournament_type cannot be blank", 5014)
        if data.get("tournament_type").isdigit():
            if not 0 <= int(data.get("tournament_type")) <= 2:
                raise CustomException("invalid value for tournament type", 5006)
        else:
            raise CustomException("tournament_type must be an Integer", 5007)

    def validate_match_type(self, data):
        if len(data.get("match_type")) == 0:
            raise CustomException("match_type cannot be blank", 5015)
        if data.get("match_type").isdigit():
            if not 0 <= int(data.get("match_type")) <= 1:
                raise CustomException("invalid value for match type", 5008)
        else:
            raise CustomException("match_type must be an Integer", 5009)

    def validate_logo_url(self, value):
        logo_file = value
        if not logo_file:
            raise CustomException("Please insert an logo", 5002)
        if type(logo_file) == str:
            if logo_file == "1":
                return
            else:
                raise CustomException("invalid value for logo_url", 4006)
        allowed = ["image/jpeg", "image/png"]
        if logo_file.content_type not in allowed:
            raise CustomException("This file type is not allowed", 4017)

        if logo_file.size > 2 * 1024 * 1024:
            raise CustomException("File size should not exceed 2 MB", 4018)

    def validate_banner_url(self, value):
        logo_file = value
        if not logo_file:
            raise CustomException("Please insert an banner", 5003)
        if type(logo_file) == str:
            if logo_file == "1":
                return
            else:
                raise CustomException("invalid value for banner_url", 4006)
        allowed = ["image/jpeg", "image/png"]
        if logo_file.content_type not in allowed:
            raise CustomException("This file type is not allowed", 4017)

        if logo_file.size > 2 * 1024 * 1024:
            raise CustomException("File size should not exceed 2 MB", 4018)

    def validate_description(self, data):
        description = data.get("description")
        print("LENGTH : ", len(description))
        if len(description) < 1 or len(description) > 500:
            raise CustomException(
                "description should not be less than 1 and exceed 500", 5010
            )

    def validate_city(self, data):
        try:
            if len(data.get("city")) == 0:
                raise CustomException("city cannot be blank", 5018)
            print(data.get("city"))
            if not data.get("city").isdigit():
                raise CustomException("city must be an Integer", 4005)
            City.objects.get(id=data.get("city"))
        except City.DoesNotExist:
            raise CustomException("City with this id is not available", 4007)

    def validate_ground(self, data):
        try:
            if len(data.get("ground")) == 0:
                raise CustomException("ground cannot be blank", 5017)
            if not data.get("ground").isdigit():
                raise CustomException("Ground must be an Integer", 5011)
            Ground.objects.get(id=data.get("ground"))
        except Ground.DoesNotExist:
            raise CustomException("Ground with this id is not available", 5012)

    def validate_flag_param(self, request):
        if len(request.query_params) != 0:
            if "flag" in request.query_params:
                if not request.query_params["flag"].isdigit():
                    raise CustomException(
                        "Invalid value for flag.please enter 0 or 1", 5020
                    )
                if (
                    request.query_params["flag"] == "0"
                    or request.query_params["flag"] == "1"
                ):
                    return
                else:
                    raise CustomException(
                        "Invalid value for flag.please enter 0 or 1", 5020
                    )
            else:
                raise CustomException("query parameter 'flag' is required", 5019)
        raise CustomException("query parameter 'flag' is required", 5019)


class CustomException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def to_dict(self):
        return {"status_code": self.error_code, "message": self.message}


def delete_tournament_validations(data):
    required_keys = ["tournament_id", "deleted_reason"]
    if set(required_keys) - set(data.keys()):
        raise DeleteTournamentCustomException(custom_errors.ERR_1052)
    if not validations.valid_tournament_id(data["tournament_id"]):
        raise DeleteTournamentCustomException(custom_errors.ERR_1038)
    if isinstance(data["deleted_reason"], str):
        if data["deleted_reason"].isspace() or data["deleted_reason"] == "":
            raise DeleteTournamentCustomException(custom_errors.ERR_1048)
        if len(data["deleted_reason"]) > 150:
            raise DeleteTournamentCustomException(custom_errors.ERR_1049)
    else:
        raise DeleteTournamentCustomException(custom_errors.ERR_1049)
    if "deleted_description" in data.keys():
        valid_delete_description(data["deleted_description"])


def valid_delete_description(description):
    if isinstance(description, str):
        if description.isspace() or description == "":
            raise DeleteTournamentCustomException(custom_errors.ERR_1050)
        if len(description) > 255:
            raise DeleteTournamentCustomException(custom_errors.ERR_1051)
    else:
        raise DeleteTournamentCustomException(custom_errors.ERR_1051)
