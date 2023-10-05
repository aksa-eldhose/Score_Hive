import datetime
import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scorehive_server.common import custom_errors
from team.models import Team
from team_players.models import TeamPlayers
from team_players.validations import CustomException
from tournament.models import Tournament

from . import team_tournament_validations
from .models import TeamTournaments

logger = logging.getLogger(__name__)


class AddTeamtoTournament(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    required_keys = ["tournament_id", "team_id"]

    def post(self, request):
        try:
            team_tournament_validations.remove_team_from_tournament_validations(
                request.data
            )
        except CustomException as ce:
            return handle_exception(ce)
        try:
            tournament_id = request.data["tournament_id"]
            team_id = request.data["team_id"]
            tournament = Tournament.objects.get(id=tournament_id, user=request.user)
            if tournament.end_date < datetime.date.today():
                return Response(
                    custom_errors.ERR_1053, status=status.HTTP_400_BAD_REQUEST
                )
            try:
                team = Team.objects.get(id=team_id)
                try:
                    TeamTournaments.objects.get(
                        tournament_id=tournament.pk, team_id=team.pk
                    )
                    logger.error({"message": "Team already in tournament"})
                    return Response(
                        custom_errors.ERR_1040, status=status.HTTP_400_BAD_REQUEST
                    )
                except ObjectDoesNotExist:
                    all_players_in_the_team = TeamPlayers.objects.filter(
                        team_id=team.pk
                    )
                    all_teams_of_all_players = Team.objects.filter(
                        team_players_team__player_id__in=all_players_in_the_team.values(
                            "player_id"
                        )
                    ).distinct()
                    all_tournaments_of_all_teams = Tournament.objects.filter(
                        teamTournament_tournament__team_id__in=all_teams_of_all_players.values(
                            "id"
                        ),
                        end_date__gte=datetime.date.today(),
                    ).distinct()
                    try:
                        self.player_check(all_tournaments_of_all_teams, tournament)
                    except CustomException as ce:
                        return handle_exception(ce)
                    try:
                        deleted_team_from_tournament = (
                            TeamTournaments.objects.get_deleted_row(
                                tournament_id=tournament, team_id=team, status=0
                            )
                        )
                        deleted_team_from_tournament.status = 1
                        deleted_team_from_tournament.save()
                    except ObjectDoesNotExist:
                        new_team_tournament = TeamTournaments(
                            tournament_id=tournament, team_id=team
                        )
                        new_team_tournament.save()
                    return Response({"message": "Team added to tournament"}, status=200)
            except ObjectDoesNotExist:
                logger.error({"message": "Team not found"})
                return Response(
                    custom_errors.ERR_4012, status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            logger.error({"message": "Tournament not found"})
            return Response(custom_errors.ERR_1039, status=status.HTTP_400_BAD_REQUEST)

    def player_check(self, all_tournaments_of_all_teams, tournament):
        for tournaments in all_tournaments_of_all_teams:
            if (
                (
                    (tournament.start_date >= tournaments.start_date)
                    and (tournament.start_date <= tournaments.end_date)
                )
                or (
                    (tournament.end_date >= tournaments.start_date)
                    and (tournament.end_date <= tournaments.end_date)
                )
                or (
                    (tournament.start_date <= tournaments.start_date)
                    and (tournament.end_date >= tournaments.end_date)
                )
            ):
                raise CustomException(
                    custom_errors.ERR_1041,
                )


class RemoveTeamFromTournament(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def put(self, request):
        try:
            team_tournament_validations.remove_team_from_tournament_validations(
                request.data
            )
        except CustomException as e:
            return handle_exception(e)
        try:
            tournament_id = request.data["tournament_id"]
            team_id = request.data["team_id"]
            tournament = Tournament.objects.get(id=tournament_id, user=request.user.id)
            if tournament.end_date < datetime.date.today():
                return Response(
                    custom_errors.ERR_1058, status=status.HTTP_400_BAD_REQUEST
                )
            try:
                team_tournament = TeamTournaments.objects.get(
                    tournament_id=tournament_id, team_id=team_id
                )
                team_tournament.status = 0
                team_tournament.save()
                return Response({"message": "Team removed from tournament"}, status=200)
            except ObjectDoesNotExist:
                return Response(custom_errors.ERR_1042, status=400)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=400)


def handle_exception(e):
    return Response(
        {"error_code": e.error_code, "message": e.message},
        status=status.HTTP_400_BAD_REQUEST,
    )
