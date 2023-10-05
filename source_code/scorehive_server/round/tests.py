from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from score.tests import generate_random_password
from scorehive_server.common import custom_errors
from team.models import City, Team
from team_tournaments.models import TeamTournaments
from tournament.models import Ground

from .models import TournamentRounds
from .views import Round, Tournament

passwd1 = generate_random_password()
passwd2 = generate_random_password()


class ListRound(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com", password=passwd1)
        self.user1 = User.objects.create(email="test1@gmail.com", password=passwd2)
        self.city = City.objects.create(name="Kottayam")
        self.ground = Ground.objects.create(name="school")
        self.round = Round.objects.create(id=1, name="round1", round_type=1)
        self.team = Team.objects.create(name="TestTeam", user=self.user, city=self.city)
        self.team1 = Team.objects.create(
            name="TestTeam1", user=self.user, city=self.city
        )
        self.tournament = Tournament.objects.create(
            name="Tournament_1",
            city=self.city,
            ground=self.ground,
            start_date="2023-08-20",
            end_date="2023-10-25",
            tournament_type=0,
            match_type=0,
            ball_type=0,
            user=self.user,
        )
        self.tournament1 = Tournament.objects.create(
            name="Tournament_2",
            city=self.city,
            ground=self.ground,
            start_date="2023-07-20",
            end_date="2023-07-25",
            tournament_type=0,
            match_type=0,
            ball_type=0,
            user=self.user1,
        )
        self.team_tournament = TeamTournaments.objects.create(
            tournament_id=self.tournament1, team_id=self.team
        )
        self.tournament_team = TeamTournaments.objects.create(
            tournament_id=self.tournament, team_id=self.team
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_round(self):
        response = self.client.get(reverse("listAllRounds"))
        self.assertEqual(response.status_code, 200)

    def test_add_round_in_tournament(self):
        response = self.client.post(reverse("addRoundsTournament"), {}, format="json")
        self.assertEqual(response.data, custom_errors.MISSING_REQUIRED_FIELDS)

        # Invalid tournament_id
        response = self.client.post(
            reverse("addRoundsTournament"),
            {"tournament_id": -1, "round_ids": [1]},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

        # Tournament id valid but no tournament found
        response = self.client.post(
            reverse("addRoundsTournament"),
            {"tournament_id": 50, "round_ids": [1]},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

        # Invalid round id
        response = self.client.post(
            reverse("addRoundsTournament"),
            {"tournament_id": self.tournament.id, "round_ids": 10},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

        # Add with valid data
        TournamentRounds.objects.create(
            tournament_id=self.tournament, round_id=self.round
        )
        response = self.client.post(
            reverse("addRoundsTournament"),
            {"tournament_id": self.tournament.id, "round_ids": [self.round.id]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        round2 = Round.objects.create(id=2, name="round2", round_type=2)
        response = self.client.post(
            reverse("addRoundsTournament"),
            {"tournament_id": self.tournament.id, "round_ids": [round2.id]},
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_list_rounds_in_tournament(self):
        # With valid request
        response = self.client.get(f"/round/{self.tournament.id}/rounds/")
        self.assertEqual(response.status_code, 200)

        # With invalid tournament_id
        response = self.client.get("/round/-2/rounds/")
        self.assertEqual(response.status_code, 400)

        # Tournament not found
        response = self.client.get("/round/500/rounds/")
        self.assertEqual(response.status_code, 400)

    def test_delete_round(self):
        # With valid data
        round3 = Round.objects.create(id=3, name="round3", round_type=2)
        TournamentRounds.objects.create(tournament_id=self.tournament, round_id=round3)
        response = self.client.put(
            reverse("addRoundsTournament"),
            {
                "tournament_id": self.tournament.id,
                "round_id": round3.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

        # Invalid tournament_id
        response = self.client.put(
            reverse("addRoundsTournament"),
            {"tournament_id": -1, "round_id": 1},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

        # Tournament id valid but no tournament found
        response = self.client.put(
            reverse("addRoundsTournament"),
            {"tournament_id": 50, "round_id": 1},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

        # Invalid round id
        response = self.client.put(
            reverse("addRoundsTournament"),
            {"tournament_id": self.tournament.id, "round_id": -10},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

        # Round not found
        response = self.client.put(
            reverse("addRoundsTournament"),
            {"tournament_id": self.tournament.id, "round_id": 100},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_rounds_in_tournament_non_paginated(self):
        # Valid request
        response = self.client.get(f"/round/{self.tournament.id}/rounds/noPaged")
        self.assertEqual(response.status_code, 200)

        # Invalid tournament id
        response = self.client.get("/round/-5/rounds/noPaged")
        self.assertEqual(response.status_code, 400)
