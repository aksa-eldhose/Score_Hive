import logging

from scorehive_server.common import custom_errors
from team_players import validations
from team_players.validations import CustomException

logger = logging.getLogger(__name__)


def remove_team_from_tournament_validations(data):
    required_keys = ["tournament_id", "team_id"]
    if set(required_keys) - set(data.keys()):
        logger.error({"message": "All fields are required"})
        raise CustomException(custom_errors.MISSING_REQUIRED_FIELDS)
    if not validations.valid_tournament_id(data["tournament_id"]):
        logger.error({"message": "Tournament_id should be a positive integer"})
        raise CustomException(custom_errors.ERR_1038)
    if not validations.valid_team_id(data["team_id"]):
        logger.error({"message": "TeamId should be a positive integer"})
        raise CustomException(custom_errors.ERR_4015)
