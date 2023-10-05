import datetime
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, CharField, F, Q, Value, When
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scorehive_server.common import custom_errors
from team.serializer import TeamSerializerII
from team_tournaments.models import TeamTournaments

from .models import Team, Tournament, TournamentGroups, TournamentGroupTeams
from .serializer import TournamentGroupSerializer
from .validations import (CustomException, valid_group_id, valid_tournament_id,
                          validate_teams)

# Create your views here.
logger = logging.getLogger(__name__)


class TournamentGroupsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TournamentGroupSerializer
    required_keys = ["tournament_id", "team_ids", "name"]

    def post(self, request):
        missing_keys = set(self.required_keys) - set(request.data.keys())
        if missing_keys:
            logger.error(custom_errors.MISSING_REQUIRED_FIELDS)
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )

        name = request.data.get("name")
        tournament_id = request.data.get("tournament_id")

        try:
            valid_tournament_id(tournament_id)
            validate_teams(request.data)
        except CustomException as e:
            return Response(
                {"error_code": e.error_code, "message": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            Tournament.objects.get(id=tournament_id, user_id=request.user.pk)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=status.HTTP_400_BAD_REQUEST)

        input_teams = request.data.get("team_ids", [])
        teams = TeamTournaments.objects.filter(tournament_id=tournament_id).values_list(
            "team_id", flat=True
        )
        teams_not_in_tournament = set(input_teams) - set(teams)

        if teams_not_in_tournament:
            return Response(
                {
                    "error_code": 1055,
                    "message": "Some teams are not in this tournament",
                    "team_ids_not_in_tournament": list(teams_not_in_tournament),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            TournamentGroups.objects.get(
                tournament_id=tournament_id, name=name, status=1
            )
            logger.error({"message": "Group already exists"})
            return Response(custom_errors.ERR_1056, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass

        all_groups = TournamentGroups.objects.filter(
            tournament_id=tournament_id, status=1
        )
        for group in all_groups:
            teams = TournamentGroupTeams.objects.filter(
                group_id=group.id, status=1
            ).values_list("team_id", flat=True)
            common_team_ids = set(request.data.get("team_ids", [])) & set(teams)
            if common_team_ids:
                return Response(
                    {
                        "message": f"Teams already in group {group.id}: {list(common_team_ids)}",
                        "error_code": 2003,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        logger.info({"message": "No groups with this name"})
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            group = serialized_data.save()
            team_ids = request.data.get("team_ids", [])
            for team_id in team_ids:
                team = Team.objects.get(id=team_id)
                tournament_group_team = TournamentGroupTeams(
                    group_id=group, team_id=team
                )
                tournament_group_team.save()

            return Response({"message": "Group added"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": serialized_data.errors, "error_code": 4001},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, tournament_id):
        logger.info(request)
        try:
            tournament_id = int(tournament_id)
            if tournament_id <= 0:
                return Response(
                    custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST)
        try:
            Tournament.objects.get(id=tournament_id, user=request.user.id)
            groups = TournamentGroups.objects.filter(
                tournament_id=tournament_id
            ).order_by("-updated_at")
            if len(groups) == 0:
                return Response(
                    custom_errors.ERR_4014, status=status.HTTP_400_BAD_REQUEST
                )
            response_data = []
            for group in groups:
                teams = TournamentGroupTeams.objects.filter(
                    group_id=group.id, team_id__status=0, status=1
                ).order_by("-updated_at")
                teams = TeamTournaments.objects.filter(
                    tournament_id=tournament_id,
                    team_id__in=teams.values_list("team_id", flat=True),
                ).values_list("team_id", flat=True)
                team_data = teams.values(
                    "team_id", name=F("team_id__name"), logo_url=F("team_id__logo_url")
                )
                group_data = {
                    "id": group.id,
                    "name": group.name,
                    "teams": team_data,
                }
                response_data.append(group_data)

            return Response(response_data)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        logger.info(request)
        required_keys = ["tournament_id", "team_ids", "name", "group_id"]
        missing_keys = set(required_keys) - set(request.data.keys())
        if missing_keys:
            logger.error({"message": "All fields are required"})
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )

        name = request.data.get("name")
        tournament_id = request.data.get("tournament_id")
        try:
            valid_tournament_id(tournament_id)
            validate_teams(request.data)
        except CustomException as e:
            return Response(
                {"error_code": e.error_code, "message": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tournament = Tournament.objects.get(
                id=tournament_id, user_id=request.user.pk
            )
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=status.HTTP_400_BAD_REQUEST)

        if tournament.end_date < datetime.date.today():
            return Response(custom_errors.ERR_1060, status=status.HTTP_400_BAD_REQUEST)

        if not valid_group_id(request.data["group_id"]):
            return Response(custom_errors.ERR_1059, status=status.HTTP_400_BAD_REQUEST)
        try:
            TournamentGroups.objects.get(
                id=request.data.get("group_id"),
                tournament_id=request.data.get("tournament_id"),
                status=1,
            )
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1063, status=status.HTTP_400_BAD_REQUEST)
        input_teams = request.data.get("team_ids", [])
        teams = TeamTournaments.objects.filter(tournament_id=tournament_id).values_list(
            "team_id", flat=True
        )
        teams_not_in_tournament = set(input_teams) - set(teams)

        if teams_not_in_tournament:
            return Response(
                {
                    "error_code": 1055,
                    "message": "Some teams are not in this tournament",
                    "team_ids_not_in_tournament": list(teams_not_in_tournament),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        all_groups = TournamentGroups.objects.filter(
            tournament_id=tournament_id, status=1
        )
        for group in all_groups:
            if group.id == request.data.get("group_id"):
                continue
            teams = TournamentGroupTeams.objects.filter(
                group_id=group.id, status=1
            ).values_list("team_id", flat=True)
            common_team_ids = set(request.data.get("team_ids", [])) & set(teams)
            if common_team_ids:
                return Response(
                    {
                        "message": f"Teams already in group {group.id}: {list(common_team_ids)}",
                        "error_code": 2003,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        logger.info({"message": "No groups with this name"})
        if self.group_exist(request.data.get("group_id"), name, tournament_id):
            return Response(custom_errors.ERR_1056, status=status.HTTP_400_BAD_REQUEST)
        serialized_data = self.serializer_class(data=request.data)
        serialized_data.is_valid()
        if "name" not in serialized_data.errors:
            self.save_group_teams(request.data.get("group_id"), name, request)

            return Response({"message": "Group updated"})
        else:
            return Response(
                {"message": serialized_data.errors, "error_code": 4001},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def group_exist(self, group, name, tournament_id):
        try:
            exist = TournamentGroups.objects.get(
                tournament_id=tournament_id, name=name, status=1
            )
            if exist.id != group:
                return True
        except ObjectDoesNotExist:
            return False

    def save_group_teams(self, group_id, name, request):
        group = TournamentGroups.objects.get(id=group_id)
        group.name = name
        group.save()
        team_ids = request.data.get("team_ids", [])
        existing_teams = TournamentGroupTeams.objects.filter(
            Q(group_id=group.id) & (Q(status=0) | Q(status=1))
        )
        existing_team_ids = set(existing_teams.values_list("team_id", flat=True))
        for team_id in team_ids:
            if team_id in existing_team_ids:
                tournament_group_team = existing_teams.get(team_id=team_id)
                if tournament_group_team.status == 0:
                    tournament_group_team.status = 1
                    tournament_group_team.save()
                existing_team_ids.remove(team_id)
            else:
                team = Team.objects.get(id=team_id)
                tournament_group_team = TournamentGroupTeams(
                    group_id=group, team_id=team, status=1
                )
                tournament_group_team.save()
        TournamentGroupTeams.objects.filter(
            group_id=group.id, team_id__in=existing_team_ids
        ).update(status=0)


class TournamentGroupDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            if not valid_group_id(int(group_id)):
                return Response(
                    custom_errors.ERR_1059, status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(custom_errors.ERR_1059, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = TournamentGroups.objects.get(id=group_id)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1063, status=status.HTTP_400_BAD_REQUEST)
        try:
            logger.info(group.tournament_id)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=status.HTTP_400_BAD_REQUEST)
        tournament_teams = TeamTournaments.objects.filter(
            tournament_id=group.tournament_id, team_id__status=0, status=1
        ).values_list("team_id", flat=True)
        group_teams = TournamentGroupTeams.objects.filter(
            group_id=group_id, status=1
        ).values_list("team_id", flat=True)
        teams = set(group_teams) & set(tournament_teams)
        team_data = TournamentGroupTeams.objects.filter(
            group_id=group_id, status=1, team_id__in=teams
        ).values(
            city=F("team_id__city__name"),
            team=F("team_id"),
            name=F("team_id__name"),
            logo_url=Case(
                When(team_id__logo_url="", then=Value("")),
                default=Concat(
                    Value("/"), F("team_id__logo_url"), output_field=CharField()
                ),
                output_field=CharField(),
            ),
        )
        group_data = {
            "id": group.id,
            "name": group.name,
            "teams": team_data,
        }
        return Response(group_data)


class DeleteGroupView(APIView):
    permission_classes = [IsAuthenticated]
    required_keys = ["tournament_id", "group_id"]

    def put(self, request):
        missing_keys = set(self.required_keys) - set(request.data.keys())
        if missing_keys:
            logger.error({"message": "All fields are required"})
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )
        tournament_id = request.data.get("tournament_id")
        group_id = request.data.get("group_id")

        try:
            valid_tournament_id(tournament_id)
        except CustomException as e:
            return Response(
                {"error_code": e.error_code, "message": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not valid_group_id(group_id):
            return Response(custom_errors.ERR_1059, status=status.HTTP_400_BAD_REQUEST)
        try:
            tournament = Tournament.objects.get(
                id=tournament_id, user_id=request.user.pk
            )
            if tournament.end_date < datetime.date.today():
                return Response(
                    custom_errors.ERR_1060, status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = TournamentGroups.objects.get(id=group_id)
            group.status = 0
            group.save()
            return Response({"message": "Group removed from tournament"})
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_4014)


class TournamentGroupTeamListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_id):
        logger.info(request)
        try:
            tournament_id = int(tournament_id)
            if tournament_id <= 0:
                return Response(
                    custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST)
        try:
            tournament = Tournament.objects.get(id=tournament_id, user=request.user.id)
            groups = TournamentGroups.objects.filter(tournament_id=tournament, status=1)
            team_grouped = TournamentGroupTeams.objects.filter(
                group_id__in=groups
            ).values_list("team_id", flat=True)
            all_ids = TeamTournaments.objects.filter(
                tournament_id=tournament
            ).values_list("team_id", flat=True)
            ungrouped = (
                Team.objects.filter(id__in=all_ids)
                .exclude(id__in=team_grouped)
                .order_by("-updated_at")
            )
            data = TeamSerializerII(ungrouped, many=True)
            return Response(data.data)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=status.HTTP_400_BAD_REQUEST)
