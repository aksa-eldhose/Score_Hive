from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team_players.models import TeamPlayers
from team_tournaments.models import TeamTournaments

from .models import City, Team
from .serializer import CitySerializer, TeamSerializer, TeamSerializerII
from .validations import CustomException, TeamValidations

message1 = "Team not found"


# Create your views here.
class TeamView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def post(self, request):
        try:
            team_validations = TeamValidations()
            team_validations.team_data_validation(request)
            data = request.data.copy()
            data["user"] = request.user.id
            team_serializer = TeamSerializer(data=data)
            if team_serializer.is_valid():
                team_serializer.save()
                return Response(team_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"message": team_serializer.errors, "error_code": 4001},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            team_validations = TeamValidations()
            team_validations.team_id_param(request)
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)
        try:
            team = Team.objects.get(
                id=request.query_params.get("id"), user=request.user.id
            )
        except Team.DoesNotExist:
            return Response(
                {"message": message1, "error_code": "4012"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            team_validations = TeamValidations()
            team_validations.team_data_validation(request)
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)
        try:
            data = request.data.copy()
            if "logo_url" in data and data["logo_url"] == "1":
                team.logo_url.delete(save=False)
                data.pop("logo_url")
            team_serializer = TeamSerializer(team, data, partial=True)
            if team_serializer.is_valid():
                team_serializer.save()
                return Response(team_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": team_serializer.errors, "error_code": 4001},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return handle_exception(str(e), 4014)

    def get(self, request):
        try:
            team_validations = TeamValidations()
            team_validations.validate_query_param(request)
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)

        teams = Team.objects.filter(user=request.user.id).order_by("-created_at")
        if teams.count() == 0:
            return Response(
                {"message": "Teams not found", "error_code": "4012"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(teams, request)
        except Exception as e:
            return handle_exception(str(e), 4013)
        try:
            data = TeamSerializerII(paginated_queryset, many=True).data
            return paginator.get_paginated_response(data)
        except Exception as e:
            return handle_exception(str(e), 4014)

    def delete(
        self,
        request,
    ):
        try:
            team_validations = TeamValidations()
            team_validations.team_id_param(request)
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)

        try:
            team = Team.objects.get(
                id=request.query_params.get("id"), user=request.user.id
            )
        except Team.DoesNotExist:
            return Response(
                {"message": message1, "error_code": "4012"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            TeamTournaments.objects.filter(
                team_id=request.query_params.get("id")
            ).update(status=0)
            TeamPlayers.objects.filter(team_id=request.query_params.get("id")).update(
                status=0
            )
            team_serializer = TeamSerializer(team, {"status": "1"}, partial=True)
            if team_serializer.is_valid():
                team_serializer.save()
                return Response(
                    {"message": "Successfully deleted"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": team_serializer.errors, "error_code": 4001},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def handle_exception(exception, error_code):
    return Response(
        {"message": str(exception), "error_code": error_code},
        status=status.HTTP_400_BAD_REQUEST,
    )


class CityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cities = City.objects.all()
            data = CitySerializer(cities, many=True)
            return Response(data.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e), "error_code": "4016"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TeamViewII(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            team = Team.objects.get(id=id)
        except Team.DoesNotExist:
            return Response(
                {"message": message1, "error_code": "4012"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            data = TeamSerializerII(team)
            return Response(data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e), "error_code": "4016"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PlayerTeamsView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            team_validations = TeamValidations()
            team_validations.validate_query_param(request)
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)
        playing_teams_record = TeamPlayers.objects.filter(
            player_id=request.user.id, status=1
        ).order_by("-created_at")
        if playing_teams_record.count() == 0:
            return Response(
                {"message": "Teams not found", "error_code": "4012"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            teams = [record.team_id for record in playing_teams_record]
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(teams, request)
        except Exception as e:
            return handle_exception(str(e), 4013)
        try:
            data = TeamSerializerII(paginated_queryset, many=True).data
            return paginator.get_paginated_response(data)
        except Exception as e:
            return handle_exception(str(e), 4014)
