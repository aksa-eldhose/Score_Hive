"""
Follow this standard for defining new custom errors

Range 1001-1999
Input validation errors

Range 2001-2999
Inputs ok db errors like constraints

Range 3001-3999
external errors like mail sending connections etc

Range 4001-4999
"""

MISSING_REQUIRED_FIELDS = {"error_code": 1001, "message": "All fields are required"}

USER_ALREADY_EXISTS = {
    "error_code": 2001,
    "message": "User with this email already exist",
}
USER_DOESNOT_EXISTS = {
    "error_code": 2002,
    "message": "No user account found associated with the given mail",
}
ERR_1003 = {
    "error_code": 1003,
    "message": "Maximum length of email should be 100 characters",
}
ERR_1008 = {"error_code": 1008, "message": "Token invalid or expired"}
ERR_1009 = {"error_code": 1009, "message": "Invalid credentials"}
ERR_1025 = {"error_code": 1025, "message": "team_id is required"}
ERR_1027 = {
    "error_code": 1027,
    "message": "User is already member of the team",
}
ERR_1029 = {
    "error_code": 1029,
    "message": "Invitation link sending failed",
}
ERR_1038 = {"error_code": 1038, "message": "Tournament_id should be a positive integer"}
ERR_1039 = {"error_code": 1039, "message": "Tournament not found"}
ERR_1040 = {"error_code": 1040, "message": "Team already in tournament"}
ERR_1041 = {
    "error_code": 1041,
    "message": "Some team members have other tournaments in same dates for other teams",
}
ERR_1042 = {"error_code": 1042, "message": "Team not in tournament"}
ERR_1044 = {
    "error_code": 1044,
    "message": "Some other teams which the player is already member have"
    " tournaments in same date as this new team",
}
ERR_1046 = {
    "error_code": 1046,
    "message": "player_ids need to be a list of positive integers",
}

ERR_4012 = {"error_code": 4012, "message": "Team not found"}
ERR_4014 = {"error_code": 4014, "message": "Groups not found"}
ERR_4015 = {"error_code": 4015, "message": "team_id should be a positive integer"}
ERR_4016 = {"error_code": 4016, "message": "Round not found"}
ERR_4017 = {"error_code": 4017, "message": "round_id should be a positive integer"}

ERR_1048 = {"error_code": 1048, "message": "deleted_reason should not be blank"}
ERR_1049 = {
    "error_code": 1049,
    "message": "deleted_reason should be a string of maximum length 150 characters",
}
ERR_1050 = {"error_code": 1050, "message": "deleted_description should not be blank"}
ERR_1051 = {
    "error_code": 1051,
    "message": "deleted_description should be a string of maximum length 255 characters",
}
ERR_1052 = {
    "error_code": 1052,
    "message": "tournament_id and deleted_reason are required",
}
ERR_1053 = {"error_code": 1053, "message": "Tournament already finished"}
ERR_1056 = {"error_code": 1056, "message": "Group already exists with this name"}
ERR_1057 = {
    "error_code": 1057,
    "message": "team_ids need to be a list of positive integers",
}
ERR_1058 = {"error_code": 1058, "message": "Cannot remove team from ended tournament"}
ERR_1063 = {"error_code": 1063, "message": "Group not found"}
ERR_1059 = {"error_code": 1059, "message": "group_id should be a positive integer"}
ERR_1060 = {"error_code": 1060, "message": "Cannot edit groups of ended tournament"}
ERR_1062 = {"error_code": 1062, "message": "Round not in tournament"}
ERR_1064 = {
    "error_code": 1064,
    "message": "round_ids need to be a list of positive integers",
}
ERR_1078 = {"error_code": 1078, "message": "Team not found / Team not in group"}
ERR_1079 = {"error_code": 1079, "message": "Tournament ended"}
ERR_1080 = {"error_code": 1080, "message": "Match type not valid"}
ERR_1081 = {
    "error_code": 1081,
    "message": "Over per bowler is greater than total overs",
}
ERR_1082 = {
    "error_code": 1082,
    "message": "over_per_bowler should be a positive integer",
}
ERR_1083 = {"error_code": 1083, "message": "over should be a positive integer"}
ERR_1084 = {"error_code": 1084, "message": "over is required in limited over match"}
ERR_1085 = {
    "error_code": 1085,
    "message": "over_per_bowler is required in limited over match",
}
ERR_1086 = {"error_code": 1086, "message": "Cannot schedule match for past date"}
ERR_1087 = {
    "error_code": 1087,
    "message": "Cannot schedule match after tournament end date",
}
ERR_1088 = {
    "error_code": 1088,
    "message": "Match already exists",
}
ERR_1066 = {
    "error_code": 1066,
    "message": "Match not found",
}
ERR_1067 = {"error_code": 1067, "message": "match_id should be a positive integer."}
ERR_1068 = {"message": "inning should be a positive integer.", "error_code": 1068}
ERR_1069 = {"message": "over should be a positive integer.", "error_code": 1069}
ERR_1070 = {"message": "ball_number should be a positive integer.", "error_code": 1070}
ERR_1071 = {"message": "striker_id should be a positive integer.", "error_code": 1071}
ERR_1072 = {"message": "Striker not in batting team", "error_code": 1072}
ERR_1073 = {
    "message": "non_striker_id should be a positive integer.",
    "error_code": 1073,
}
ERR_1074 = {"message": "bowler_id should be a positive integer.", "error_code": 1074}
ERR_1075 = {"message": "runs should be zero or more.", "error_code": 1075}
ERR_1089 = {"message": "Non Striker not in batting team", "error_code": 1089}
ERR_1090 = {"message": "Batting team not found in match", "error_code": 1090}
ERR_1091 = {"message": "Bowler not in team", "error_code": 1091}
ERR_1092 = {"message": "Not a valid choice for extras", "error_code": 1092}
ERR_1093 = {"message": "Striker and non-striker cannot be same", "error_code": 1093}
