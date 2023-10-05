import datetime
import logging
import os

import jwt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import EmailMessage
from django.core.validators import EmailValidator
from django.db.models import Case, F, Q, When
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import SearchUserSerializer
from scorehive_server.common import custom_errors
from team.models import Team
from tournament.models import Tournament

from . import validations
from .models import TeamPlayers
from .validations import CustomException

logger = logging.getLogger(__name__)
invitation_sent = {"message": "Invitation link sent"}
invitation_failed = {"message": "Invitation link sending failed"}


class PlayerList(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, teamid):
        logger.info(request)
        logger.info("teamid = " + teamid)
        if teamid.isdigit():
            try:
                Team.objects.get(id=teamid)
                team_players = TeamPlayers.objects.filter(team_id=teamid, status=1)
                team_players = team_players.values(
                    "player_id",
                    name=F("player_id__name"),
                    email=F("player_id__email"),
                    phone_number=F("player_id__phone_number"),
                )
                logger.info(list(team_players))
                return Response(list(team_players))
            except ObjectDoesNotExist:
                logger.error(custom_errors.ERR_4012)
                return Response(
                    custom_errors.ERR_4012,
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as e:
                logger.exception(e)
                return Response(status=400)
        else:
            logger.error(custom_errors.ERR_4015)
            return Response(
                custom_errors.ERR_4015,
                status=status.HTTP_400_BAD_REQUEST,
            )


class SearchPlayer(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    required_keys = ["email", "team_id"]
    serializer_class = SearchUserSerializer

    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        missing_keys = set(self.required_keys) - set(request.data.keys())
        if missing_keys:
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )
        email = request.data["email"]
        team_id = request.data["team_id"]
        if len(email) > 100:
            logger.error(custom_errors.ERR_1003)
            return Response(
                custom_errors.ERR_1003,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if isinstance(team_id, int) and team_id > 0:
            try:
                Team.objects.get(id=team_id, user=request.user)
                try:
                    TeamPlayers.objects.get(team_id=team_id, player_id__email=email)
                    return Response(
                        custom_errors.ERR_1027,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except ObjectDoesNotExist:
                    result = TeamPlayers.objects.filter(team_id=team_id)
                    result = User.objects.exclude(id__in=result.values("player_id"))
                    result = result.filter(
                        Q(email=email) | Q(email__contains=email), status=1
                    ).order_by(
                        Case(
                            When(email=email, then=0),
                            When(email__startswith=email, then=1),
                            default=2,
                        )
                    )
                    if result.count():
                        return Response(
                            {"message": self.serializer_class(result, many=True).data},
                            status=200,
                        )
                    else:
                        return Response(
                            {
                                "error_code": 1043,
                                "message": "No email matching the search",
                            },
                            status=400,
                        )
            except ObjectDoesNotExist:
                logger.error(custom_errors.ERR_4012)
                return Response(
                    custom_errors.ERR_4012,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            logger.error(custom_errors.ERR_4015)
            return Response(
                custom_errors.ERR_4015,
                status=status.HTTP_400_BAD_REQUEST,
            )


class CheckPlayerTeamMember(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        if "team_id" not in request.data:
            return Response(
                custom_errors.ERR_1025,
                status=status.HTTP_400_BAD_REQUEST,
            )
        if isinstance(request.data["team_id"], int) and request.data["team_id"] > 0:
            team_id = request.data["team_id"]
            try:
                Team.objects.get(id=team_id)
                try:
                    TeamPlayers.objects.get(
                        team_id=team_id, player_id=request.user.pk, status=1
                    )
                    logger.error({"message": "User is already member of the team"})
                    return Response(
                        custom_errors.ERR_1027,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except ObjectDoesNotExist:
                    logger.info({"message": "Player not member of team"})
                return Response(
                    {"message": "Player not member of team"},
                    status=status.HTTP_202_ACCEPTED,
                )
            except ObjectDoesNotExist as e:
                logger.error(custom_errors.ERR_4012)
                logger.exception(e)
                return Response(
                    custom_errors.ERR_4012,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            logger.error(custom_errors.ERR_4015)
            return Response(
                custom_errors.ERR_4015,
                status=status.HTTP_400_BAD_REQUEST,
            )


class PlayerJoinToTeam(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        try:
            validations.validate_team_id(request.data)
            team_id = request.data["team_id"]
            team = validations.check_if_team_valid(team_id)
            team_player = validations.check_if_user_already_team_member(
                team_id, request.user.pk
            )
            if team_player:
                raise CustomException(validations.ERROR_1027)
            else:
                if check_date_conflicts_of_player(player=request.user, new_team=team):
                    validations.add_player_to_team(team, request.user)
                    message = {"message": "Player joined in team"}
                    logger.info(message)
                    return Response(message, status=202)
                else:
                    return Response(validations.ERROR_1044, status=400)
        except CustomException as ce:
            return handle_exception(ce)


class InvitePlayerToTeam(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        logger.info(request)
        logger.info(request.data)
        return self.process_registration(request.data, request)

    def process_registration(self, data, request):
        try:
            email, team_id = self.extract_data(data)
            user = self.get_user_by_email(email)
            if user:
                return Response(custom_errors.USER_ALREADY_EXISTS, status=409)
            if len(email) > 100:
                return Response(
                    custom_errors.ERR_1003, status=status.HTTP_400_BAD_REQUEST
                )
            self.validate_email(email)
            if team_id > 0:
                team = self.get_team(team_id)
                token = self.generate_token(email, team_id)
                self.send_email_verification(email, token, team, request.user.name)
                return Response("Invitation sent", status=status.HTTP_200_OK)
            else:
                return Response(
                    custom_errors.ERR_4015, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(str(e))
            return Response(custom_errors.ERR_1029, status=status.HTTP_400_BAD_REQUEST)

    def extract_data(self, data):
        if "email" not in data or "team_id" not in data:
            raise ValidationError(custom_errors.MISSING_REQUIRED_FIELDS)
        email = data["email"]
        team_id = data["team_id"]
        if not isinstance(team_id, int):
            raise ValidationError(custom_errors.ERR_4015)
        return email, team_id

    def get_user_by_email(self, email):
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            return None

    def validate_email(
        self,
        email,
    ):
        validator = EmailValidator()
        validator(email)

    def get_team(self, team_id):
        try:
            return Team.objects.get(id=team_id)
        except ObjectDoesNotExist:
            raise ValidationError(custom_errors.ERR_4012)

    def generate_token(self, email, team_id):
        payload = {
            "email": email,
            "team_id": team_id,
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.now(),
            "purpose": "email_verification_token",
        }
        return jwt.encode(
            payload, os.environ.get("EMAIL_VERIFICATION_SECRET"), algorithm="HS256"
        )

    def send_email_verification(self, email, token, team, user_name):
        link = os.environ.get("UI_BASE_URL") + "/register-email-response/" + token + "/"
        context = {
            "verification_link": link,
            "team_name": team.name,
            "user_name": user_name,
        }
        template = "player_invite_email_verification_mail_template.html"
        email_content = render_to_string(template, context)
        email_message = EmailMessage("Register your email", email_content, to=[email])
        email_message.content_subtype = "html"
        if os.environ.get("EMAIL_SERVICES_ACTIVE") == "True":
            email_message.send()


class InviteExistingPlayerToTeam(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    required_keys = ["team_id", "player_id", "team_join_link"]

    def post(self, request):
        missing_keys = set(self.required_keys) - set(request.data.keys())
        try:
            validations.validate_req(request)
        except CustomException as e:
            return Response(
                {"error_code": e.error_code, "message": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        team_id = request.data["team_id"]
        player_id = request.data["player_id"]
        team_join_link = request.data["team_join_link"]
        if missing_keys:
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            team = Team.objects.get(id=team_id, user=request.user)
            try:
                player = User.objects.get(id=player_id, status=1)
                try:
                    TeamPlayers.objects.get(
                        team_id=team.pk, player_id=player.pk, status=1
                    )
                    return Response(
                        {
                            "error_code": 1033,
                            "message": "Player already member of team",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                except ObjectDoesNotExist:
                    if check_date_conflicts_of_player(player, team):
                        context = {
                            "team_join_link": team_join_link,
                            "team_name": team.name,
                            "user_name": request.user.name,
                        }
                        template = "existing_player_invite_email_verification_mail_template.html"
                        email_content = render_to_string(template, context)
                        email = EmailMessage(
                            "Invitation to team", email_content, to=[player.email]
                        )
                        email.content_subtype = "html"
                        try:
                            if os.environ.get("EMAIL_SERVICES_ACTIVE") == "True":
                                email.send()
                            logger.info(invitation_sent)
                            return Response(
                                invitation_sent,
                                status=status.HTTP_200_OK,
                            )
                        except Exception as e:
                            logger.error(invitation_failed)
                            logger.exception(e)
                            return Response(
                                custom_errors.ERR_1029,
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    else:
                        return Response(
                            custom_errors.ERR_1044,
                            status=status.HTTP_400_BAD_REQUEST,
                        )
            except ObjectDoesNotExist:
                return Response(
                    {"error_code": 1032, "message": "Player not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ObjectDoesNotExist:
            return Response(
                custom_errors.ERR_4012,
                status=status.HTTP_400_BAD_REQUEST,
            )


def check_date_conflicts_of_player(player, new_team):
    new_team_tournaments = Tournament.objects.filter(
        teamTournament_tournament__team_id=new_team.pk,
        end_date__gte=datetime.date.today(),
    )
    current_teams_of_player = TeamPlayers.objects.filter(
        player_id=player.pk, team_id__status=0, status=1
    )
    for team in current_teams_of_player:
        current_team_tournaments = Tournament.objects.filter(
            teamTournament_tournament__team_id=team.team_id,
            end_date__gte=datetime.date.today(),
        )
        for new_tournament in new_team_tournaments:
            for current_tournament in current_team_tournaments:
                if (
                    (
                        (new_tournament.start_date >= current_tournament.start_date)
                        and (new_tournament.start_date <= current_tournament.end_date)
                    )
                    or (
                        (new_tournament.end_date >= current_tournament.start_date)
                        and (new_tournament.end_date <= current_tournament.end_date)
                    )
                    or (
                        (new_tournament.start_date <= current_tournament.start_date)
                        and (new_tournament.end_date >= current_tournament.end_date)
                    )
                ):
                    return False
    return True


class RemovePlayerFromTeam(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    required_keys = ["player_ids", "team_id"]

    def put(self, request):
        try:
            validations.remove_player_from_team_validations(request.data)
        except CustomException as ce:
            return handle_exception(ce)
        try:
            team_id = request.data["team_id"]
            player_ids = request.data["player_ids"]
            Team.objects.get(id=team_id, user=request.user)
            players_to_delete = TeamPlayers.objects.filter(
                player_id__in=player_ids, team_id=team_id
            )
            missing_ids = set(player_ids) - set(
                players_to_delete.values_list("player_id", flat=True)
            )
            if missing_ids:
                return Response(
                    {
                        "error_code": 1047,
                        "message": "Some players are not member of team",
                        "player_ids_not_member_of_team": missing_ids,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            players_to_delete.update(status=0)
            return Response({"message": "Players removed from team"}, status=200)
        except ObjectDoesNotExist:
            logger.error(custom_errors.ERR_4012)
            return Response(custom_errors.ERR_4012, status=status.HTTP_400_BAD_REQUEST)


class ExitPlayerFromTeam(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def put(self, request, team_id):
        try:
            team_id = int(team_id)
            validations.valid_player_id(team_id)
        except ValueError:
            return Response(custom_errors.ERR_4015, status=status.HTTP_400_BAD_REQUEST)
        try:
            team = Team.objects.get(id=team_id)
            team_player = TeamPlayers.objects.get(
                team_id=team.id, player_id=request.user.id
            )
            team_player.status = 0
            team_player.save()
            return Response({"message": "Player exited from team"})
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_4012, status=status.HTTP_400_BAD_REQUEST)


def handle_exception(e):
    return Response(
        {"error_code": e.error_code, "message": e.message},
        status=status.HTTP_400_BAD_REQUEST,
    )
