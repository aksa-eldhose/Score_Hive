from group.validations import CustomException
from scorehive_server.common import custom_errors


def validate_rounds(data):
    if isinstance(data["round_ids"], list) and len(data["round_ids"]):
        for round_id in data["round_ids"]:
            if not valid_round_id(round_id):
                raise CustomException(custom_errors.ERR_1057)
    else:
        raise CustomException(custom_errors.ERR_1057)


def valid_round_id(round_id):
    return isinstance(round_id, int) and round_id > 0
