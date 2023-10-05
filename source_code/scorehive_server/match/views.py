import logging

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from scorehive_server.common import custom_errors
from team.models import City, Team
from team.serializer import CitySerializer, TeamSerializerII
from tournament.models import Ground, Tournament
from tournament.serializer import GroundSerializer

from .models import Matches
from .serializer import MatchSerializer, MatchSerializerII
from .validations import (CustomException, valid_tournament_id,
                          validate_match_id, validate_request)

# Create your views here.
logger = logging.getLogger(__name__)


class MatchesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatchSerializer
    pagination_class = PageNumberPagination

    required_keys = [
        "tournament_id",
        "team1",
        "team2",
        "match_type",
        "date_time",
        "round_id",
        "city",
        "ground",
    ]

    def post(self, request):
        missing_keys = set(self.required_keys) - set(request.data.keys())
        if missing_keys:
            logger.error(custom_errors.MISSING_REQUIRED_FIELDS)
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            validate_request(request)
        except CustomException as e:
            return Response(
                {"error_code": e.error_code, "message": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            city = request.data["city"].title()
            city_serializer = CitySerializer(data={"name": city})
            if city_serializer.is_valid():
                city, created = City.objects.get_or_create(
                    name=city, defaults={"status": 1}
                )
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
                ground, created = Ground.objects.get_or_create(
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
            data["city_id"] = city.id
            data["ground_id"] = ground.id
            data["ball_type"] = Tournament.objects.get(
                id=request.data["tournament_id"]
            ).ball_type
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            test_1 = Matches.objects.filter(
                team1=data["team1"],
                team2=data["team2"],
                round_id=data["round_id"],
                tournament_id=data["tournament_id"],
                status=1,
            )
            test_2 = Matches.objects.filter(
                team1=data["team2"],
                team2=data["team1"],
                round_id=data["round_id"],
                tournament_id=data["tournament_id"],
                status=1,
            )
            if len(test_1) > 0 or len(test_2) > 0:
                return Response(
                    custom_errors.ERR_1088, status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            pass
        serialized_data = self.serializer_class(data=data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({"message": "Match created"})
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, tournament_id):
        try:
            if not isinstance(int(tournament_id), int) and tournament_id > 0:
                return Response(
                    custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST)
        list_match = Matches.objects.filter(
            tournament_id=tournament_id, status=1
        ).order_by("-updated_at")
        paginator = self.pagination_class()
        paginator.paginate_queryset(list_match, request)
        serialized = MatchSerializerII(list_match, many=True).data
        return paginator.get_paginated_response(serialized)

    def delete(self, request, match_id):
        try:
            match_id = int(match_id)
        except ValueError:
            return Response(custom_errors.ERR_1067, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_match_id(match_id)
        except CustomException as e:
            return Response(
                {"error_code": e.error_code, "message": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            match = Matches.objects.get(id=match_id, status=1)
            match.status = 0
            match.save()
            return Response({"message": "Match deleted"})
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1066, status=status.HTTP_400_BAD_REQUEST)
