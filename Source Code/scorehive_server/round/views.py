import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from group.validations import valid_tournament_id
from scorehive_server.common import custom_errors
from tournament.models import Tournament

from .models import Round, TournamentRounds
from .serializer import RoundSerializer
from .validations import CustomException, valid_round_id, validate_rounds

logger = logging.getLogger(__name__)


# Create your views here.
class AllRoundsInTournament(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tournament_id):
        try:
            valid_tournament_id(int(tournament_id))
        except CustomException:
            return Response(custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST)
        try:
            rounds = (
                TournamentRounds.objects.filter(tournament_id=tournament_id, status=1)
                .order_by("-created_at")
                .values("id", "round_id", name=F("round_id__name"))
            )
            return Response(rounds)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_4016, status=status.HTTP_400_BAD_REQUEST)


class RoundsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            round_robin = Round.objects.filter(status=1, round_type=1).values(
                "id", "name"
            )
            knock_out = Round.objects.filter(status=1, round_type=2).values(
                "id", "name"
            )
            rounds = [{"round_robin": round_robin}, {"knock_out": knock_out}]
            return Response(rounds)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_4016, status=status.HTTP_400_BAD_REQUEST)


class TournamentRoundsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoundSerializer
    pagination_class = PageNumberPagination
    required_keys = ["tournament_id", "round_ids"]

    def post(self, request):
        missing_keys = set(self.required_keys) - set(request.data.keys())
        if missing_keys:
            logger.error(custom_errors.MISSING_REQUIRED_FIELDS)
            return Response(
                custom_errors.MISSING_REQUIRED_FIELDS,
                status=status.HTTP_400_BAD_REQUEST,
            )
        tournament_id = request.data.get("tournament_id")

        try:
            valid_tournament_id(tournament_id)
        except CustomException as e:
            return Response(
                {"error_code": e.error_code, "message": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            tournament = Tournament.objects.get(
                id=tournament_id, user_id=request.user.id
            )
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_rounds(request.data)
        except CustomException:
            return Response(custom_errors.ERR_1064, status=status.HTTP_400_BAD_REQUEST)
        try:
            existing_rounds = TournamentRounds.objects.filter(
                tournament_id=tournament_id
            )
            existing_round_ids = set(existing_rounds.values_list("round_id", flat=True))
            round_ids = request.data.get("round_ids")
            for _id in round_ids:
                if _id in existing_round_ids:
                    tournament_round = existing_rounds.get(round_id=_id)
                    if tournament_round.status == 0:
                        tournament_round.status = 1
                        tournament_round.save()
                    existing_round_ids.remove(_id)
                else:
                    _round = Round.objects.get(id=_id)
                    tournament_round = TournamentRounds(
                        tournament_id=tournament, round_id=_round
                    )
                    tournament_round.save()
            TournamentRounds.objects.filter(
                tournament_id=tournament_id, round_id__in=existing_round_ids
            ).update(status=0)
            return Response({"message": "Round added"})
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_4016, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, tournament_id):
        try:
            valid_tournament_id(int(tournament_id))
        except CustomException:
            return Response(custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST)
        try:
            Tournament.objects.get(id=tournament_id)
            rounds = (
                TournamentRounds.objects.filter(
                    tournament_id=tournament_id,
                    status=1,
                )
                .order_by("-created_at")
                .values("id", "round_id", name=F("round_id__name"))
            )
            paginator = self.pagination_class()
            paginated_set = paginator.paginate_queryset(rounds, request)
            return paginator.get_paginated_response(paginated_set)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_4016, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        tournament_id = request.data.get("tournament_id")
        round_id = request.data.get("round_id")
        try:
            valid_tournament_id(int(tournament_id))
        except CustomException:
            return Response(custom_errors.ERR_1038, status=status.HTTP_400_BAD_REQUEST)
        try:
            Tournament.objects.get(id=tournament_id, user_id=request.user.id)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1039, status=status.HTTP_400_BAD_REQUEST)
        if not valid_round_id(round_id):
            return Response(custom_errors.ERR_4017, status=status.HTTP_400_BAD_REQUEST)
        try:
            Round.objects.get(id=round_id)
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_4016, status=status.HTTP_400_BAD_REQUEST)
        try:
            rounds = TournamentRounds.objects.filter(
                tournament_id=tournament_id, round_id=round_id, status=1
            )
            if len(rounds.values()) == 0:
                return Response(
                    custom_errors.ERR_1062, status=status.HTTP_400_BAD_REQUEST
                )
            rounds.update(status=0)
            return Response(
                {"message": "Round removed from tournament"}, status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist:
            return Response(custom_errors.ERR_1062, status=status.HTTP_400_BAD_REQUEST)
