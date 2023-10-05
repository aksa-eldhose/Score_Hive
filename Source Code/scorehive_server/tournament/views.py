import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scorehive_server.common import custom_errors
from team.models import City, Team
from team.serializer import CitySerializer, TeamSerializerII
from team_players.validations import \
    CustomException as DeleteTournamentCustomException
from team_tournaments.models import TeamTournaments

from .models import Ground, Tournament
from .serializer import (GroundSerializer, HomeTournamentSerializer,
                         TeamTournamentSerializerII, TournamentSerializer,
                         TournamentSerializerII)
from .validations import (CustomException, TournamentValidation,
                          delete_tournament_validations)

# Create your views here.


class TournamentView(APIView):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            city_ = request.data["city"].title()
            city_serializer_ = CitySerializer(data={"name": city_})
            if city_serializer_.is_valid():
                city_, _ = City.objects.get_or_create(
                    name=city_, defaults={"status": 1}
                )
            else:
                return Response(
                    {
                        "message": {"city": city_serializer_.errors.get("name")},
                        "error_code": 4001,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ground_ = request.data["ground"].title()
            ground_serializer_ = GroundSerializer(data={"name": ground_})
            if ground_serializer_.is_valid():
                ground_, _ = Ground.objects.get_or_create(
                    name=ground_, defaults={"status": 1}
                )
            else:
                return Response(
                    {
                        "message": {"ground": ground_serializer_.errors.get("name")},
                        "error_code": 4001,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = request.data.copy()
            data["city"] = city_.id
            data["ground"] = ground_.id
            tour_validation = TournamentValidation()
            tour_validation.validate_tour_data(data)
            data["user"] = request.user.id
            tour_serializer = TournamentSerializer(data=data)
            if tour_serializer.is_valid():
                tour_serializer.save()
                return Response(tour_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"message": tour_serializer.errors, "error_code": 4001},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            tour_validation = TournamentValidation()
            tour_validation.validate_query_param(request)
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)

        tournament = Tournament.objects.filter(user=request.user.id).order_by(
            "-created_at"
        )
        if tournament.count() == 0:
            return Response(
                {"message": "Tournaments not found", "error_code": 5016},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(tournament, request)
        except Exception as e:
            return handle_exception(str(e), 4013)
        try:
            data = TournamentSerializer(paginated_queryset, many=True).data
            return paginator.get_paginated_response(data)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            tour = self.get_tournament(request)
            self.validate_tournament_dates(request, tour)
            self.validate_tournament_data(request)
            city = request.data["city"].title()
            city_serializer = CitySerializer(data={"name": city})
            if city_serializer.is_valid():
                city, _ = City.objects.get_or_create(name=city, defaults={"status": 1})
            else:
                return Response(
                    {
                        "message": {"city": city_serializer.errors.get("name")},
                        "error_code": 4001,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ground = request.data["ground"].title()
            ground_serializer = GroundSerializer(data={"name": ground})
            if ground_serializer.is_valid():
                ground, _ = Ground.objects.get_or_create(
                    name=ground, defaults={"status": 1}
                )
            else:
                return Response(
                    {
                        "message": {"ground": ground_serializer.errors.get("name")},
                        "error_code": 4001,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = request.data.copy()
            data["city"] = city.id
            data["ground"] = ground.id
            if "logo_url" in data and data["logo_url"] == "1":
                tour.logo_url.delete(save=False)
                data.pop("logo_url")
            if "banner_url" in data and data["banner_url"] == "1":
                tour.banner_url.delete(save=False)
                data.pop("banner_url")
            tour_serializer = TournamentSerializer(
                tour, data, partial=True, context={"tournament": tour}
            )
            if tour_serializer.is_valid():
                tour_serializer.save()
                return Response(tour_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": tour_serializer.errors, "error_code": 4001},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_tournament(self, request):
        tour = Tournament.objects.get(
            id=request.query_params.get("id"), user=request.user.id
        )
        if tour.end_date < datetime.date.today():
            raise CustomException(custom_errors.ERR_1053)
        if (
            tour.start_date <= datetime.date.today()
            and request.data.get("start_date")
            and str(tour.start_date) != request.data["start_date"]
        ):
            raise CustomException(
                message="Cannot update start_date of ongoing tournament",
                error_code=4001,
            )
        return tour

    def validate_tournament_dates(self, request, tour):
        tour_validation = TournamentValidation()
        tour_validation.tour_id_param(request)

    def validate_tournament_data(self, request):
        tour_validation = TournamentValidation()
        tour_validation.validate_tour_data(request.data)

    def get_or_create_city(self, request):
        city = request.data["city"].title()
        city_serializer = CitySerializer(data={"name": city})
        if city_serializer.is_valid():
            city, _ = City.objects.get_or_create(name=city, defaults={"status": 1})
        else:
            raise CustomException(
                message={"city": city_serializer.errors.get("name")}, error_code=4001
            )
        return city

    def get_or_create_ground(self, request):
        ground = request.data["ground"].title()
        ground_serializer = GroundSerializer(data={"name": ground})
        if ground_serializer.is_valid():
            ground, _ = Ground.objects.get_or_create(
                name=ground, defaults={"status": 1}
            )
        else:
            raise CustomException(
                message={"ground": ground_serializer.errors.get("name")},
                error_code=4001,
            )
        return ground

    def update_tournament_data(self, request, tour, city, ground):
        data = request.data.copy()
        data["city"] = city.id
        data["ground"] = ground.id
        if "logo_url" in data and data["logo_url"] == "1":
            tour.logo_url.delete(save=False)
            data.pop("logo_url")
        if "banner_url" in data and data["banner_url"] == "1":
            tour.banner_url.delete(save=False)
            data.pop("banner_url")
        tour_serializer = TournamentSerializer(
            tour, data, partial=True, context={"tournament": tour}
        )
        if tour_serializer.is_valid():
            tour_serializer.save()
            return tour_serializer.data
        else:
            raise CustomException(message=tour_serializer.errors, error_code=4001)


class GroundView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            ground = Ground.objects.all()
            data = GroundSerializer(ground, many=True)
            return Response(data.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e), "error_code": "5016"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TournamentViewII(APIView):
    def get(self, request, id):
        try:
            tour = Tournament.objects.get(id=id)
        except Tournament.DoesNotExist:
            return Response(
                {"message": "Tournament not found", "error_code": 5016},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            data = TournamentSerializerII(tour)
            permission = 0
            if data.data["user"] == request.user.id:
                permission = 1
            new_data = dict(data.data)
            new_data["permission"] = permission
            return Response(new_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e), "error_code": "4016"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TournamentTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            tour_validation = TournamentValidation()
            tour_validation.validate_flag_param(request)
            tournament = Tournament.objects.get(id=id)
            end_date = tournament.end_date
            search_term = request.query_params.get("search", "")
            user_teams = Team.objects.filter(
                user=request.user.id, name__icontains=search_term
            ).order_by("-updated_at")
            if end_date < datetime.date.today():
                teams_in_tour = TeamTournaments.objects.filter(
                    tournament_id=id, team_id__status__in=[0, 1]
                ).order_by("-updated_at")
            else:
                teams_in_tour = TeamTournaments.objects.filter(
                    tournament_id=id, team_id__status=0
                ).order_by("-updated_at")

            teams_in_tour_serialized = TeamTournamentSerializerII(
                teams_in_tour, many=True
            ).data
            user_teams_serialized = TeamSerializerII(user_teams, many=True).data

            # to remove team_id from the list
            teams_in_tournament = []
            for item in teams_in_tour_serialized:
                teams_in_tournament.append(item["team_id"])

            # to select team based on flag
            if request.query_params["flag"] == "0":
                user_teams_not_in_tour = [
                    d for d in user_teams_serialized if d not in teams_in_tournament
                ]
                return Response(user_teams_not_in_tour, status=status.HTTP_200_OK)
            else:
                if len(teams_in_tournament) == 0:
                    return Response(
                        {"message": "Teams not found", "error_code": "4012"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                return Response(teams_in_tournament, status=status.HTTP_200_OK)
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)
        except Exception as e:
            return Response(
                {"error": str(e), "error_code": "4016"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class HomeTournamentView(APIView):
    def get(self, request):
        try:
            tour_validation = TournamentValidation()
            tour_validation.validate_query_param(request)
        except CustomException as ex:
            return handle_exception(ex.message, ex.error_code)

        tournament = Tournament.objects.all().order_by("-created_at")
        if tournament.count() == 0:
            return Response(
                {"message": "Tournaments not found", "error_code": 5016},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            data = HomeTournamentSerializer(tournament, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def handle_exception(exception, error_code):
    return Response(
        {"message": str(exception), "error_code": error_code},
        status=status.HTTP_400_BAD_REQUEST,
    )


class DeleteTournament(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    required_keys = ["tournament_id", "deleted_reason"]

    def put(self, request):
        try:
            delete_tournament_validations(request.data)
        except DeleteTournamentCustomException as e:
            return delete_handle_exception(e)
        try:
            tournament_id = request.data["tournament_id"]
            deleted_reason = request.data["deleted_reason"]
            deleted_description = request.data.get("deleted_description", None)
            tournament = Tournament.objects.get(id=tournament_id, user=request.user)
            tournament.deleted_reason = deleted_reason
            tournament.deleted_description = deleted_description
            tournament.status = 0
            tournament.save()
            return Response({"message": "Tournament deleted successfully"}, status=200)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=400)


def delete_handle_exception(e):
    return Response(
        {"error_code": e.error_code, "message": e.message},
        status=status.HTTP_400_BAD_REQUEST,
    )


class PublicTournamentTeam(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            tournament_id = int(id)
            if not isinstance(tournament_id, int) and tournament_id > 0:
                return Response(
                    custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST)

        teams_in_tour = TeamTournaments.objects.filter(
            tournament_id=id, team_id__status=0
        ).order_by("-updated_at")

        teams_in_tour_serialized = TeamTournamentSerializerII(
            teams_in_tour, many=True
        ).data
        teams_in_tournament = []
        for item in teams_in_tour_serialized:
            teams_in_tournament.append(item["team_id"])
        return Response(teams_in_tournament)
