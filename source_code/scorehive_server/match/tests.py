from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from group.models import TournamentGroups, TournamentGroupTeams
from round.models import Round, TournamentRounds
from score.tests import generate_random_password
from scorehive_server.common import custom_errors
from team.models import Team
from team_tournaments.models import TeamTournaments
from tournament.models import City, Ground, Tournament

from .models import Matches

date_time = "2023-08-24T09:50"
passwd = generate_random_password()


class Match(APITestCase):
    def setUp(self):
        self.user_mt = User.objects.create(email="test@mail.com", password=passwd)
        self.city_mt = City.objects.create(name="Kottayam")
        self.ground_mt = Ground.objects.create(name="school")
        self.round_mt = Round.objects.create(id=1, name="round1", round_type=1)
        self.team_mt = Team.objects.create(
            name="TestTeam", user=self.user_mt, city=self.city_mt
        )
        self.team1_mt = Team.objects.create(
            name="TestTeam1", user=self.user_mt, city=self.city_mt
        )
        self.tournament_mt = Tournament.objects.create(
            name="Tournament_1",
            city=self.city_mt,
            ground=self.ground_mt,
            start_date="2023-09-20",
            end_date="2023-09-30",
            tournament_type=0,
            match_type=0,
            ball_type=0,
            user=self.user_mt,
        )

        self.tournament_team_mt = TeamTournaments.objects.create(
            tournament_id=self.tournament_mt, team_id=self.team_mt
        )
        self.tournament_team2_mt = TeamTournaments.objects.create(
            tournament_id=self.tournament_mt, team_id=self.team1_mt
        )
        self.group_mt = TournamentGroups.objects.create(
            name="Group", tournament_id=self.tournament_mt
        )
        self.group_team1_mt = TournamentGroupTeams.objects.create(
            group_id=self.group_mt, team_id=self.team_mt
        )
        self.group_team2_mt = TournamentGroupTeams.objects.create(
            group_id=self.group_mt, team_id=self.team1_mt
        )
        self.round1_mt = Round.objects.create(name="Round 1")
        self.round2_mt = Round.objects.create(name="Round 2")
        self.tournament_round_1 = TournamentRounds.objects.create(
            tournament_id=self.tournament_mt, round_id=self.round1_mt
        )
        self.tournament_round_2_mt = TournamentRounds.objects.create(
            tournament_id=self.tournament_mt, round_id=self.round2_mt
        )
        self.match_mt = Matches.objects.create(
            tournament_id=self.tournament_mt,
            team1=self.team1_mt,
            team2=self.team_mt,
            match_type=1,
            date_time=date_time,
            round_id=self.round2_mt,
            city_id=self.city_mt,
            ground_id=self.ground_mt,
            over_per_bowler=2,
            total_overs=6,
            ball_type=self.tournament_mt.ball_type,
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user_mt)

    def test_missing_fields(self):
        response = self.client.post(reverse("scheduleMatch"), {}, format="json")
        self.assertEqual(response.data, custom_errors.MISSING_REQUIRED_FIELDS)

    def test_invalid_request_body(self):
        response = self.client.post(
            reverse("scheduleMatch"),
            {
                "tournament_id": "invalid",
                "team1": 29,
                "team2": 27,
                "match_type": "1",
                "date_time": date_time,
                "round_id": 3,
                "over_per_bowler": 0,
                "total_overs": 0,
                "city": "Muvattupuzha",
                "ground": "school",
            },
            format="json",
        )
        self.assertEqual(response.data, custom_errors.ERR_1038)
        self.assertEqual(response.status_code, 400)

    def test_invalid_city(self):
        response = self.client.post(
            reverse("scheduleMatch"),
            {
                "tournament_id": self.tournament_mt.id,
                "team1": self.team_mt.id,
                "team2": self.team1_mt.id,
                "match_type": "1",
                "date_time": date_time,
                "round_id": self.round1_mt.id,
                "over_per_bowler": 0,
                "total_overs": 0,
                "city": "",
                "ground": "school",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_ground(self):
        response = self.client.post(
            reverse("scheduleMatch"),
            {
                "tournament_id": self.tournament_mt.id,
                "team1": self.team_mt.id,
                "team2": self.team1_mt.id,
                "match_type": "1",
                "date_time": date_time,
                "round_id": self.round1_mt.id,
                "over_per_bowler": 0,
                "total_overs": 0,
                "city": "Kottayam",
                "ground": "",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_valid_data(self):
        response = self.client.post(
            reverse("scheduleMatch"),
            {
                "tournament_id": self.tournament_mt.id,
                "team1": self.team_mt.id,
                "team2": self.team1_mt.id,
                "match_type": "1",
                "date_time": "2023-09-28T09:50",
                "round_id": self.round1_mt.id,
                "over_per_bowler": 0,
                "total_overs": 0,
                "city": "Thodupuzha",
                "ground": "School",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_list_match(self):
        response = self.client.get(f"/match/{self.tournament_mt.id}/list/")
        self.assertEqual(response.status_code, 200)

    def test_list_match_invalid_id(self):
        response = self.client.get("/match/'invalid'/list/")
        self.assertEqual(response.status_code, 400)

    def test_delete_match(self):
        response = self.client.delete(f"/match/{self.match_mt.id}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_delete_match_invalid_id(self):
        response = self.client.delete("/match/'invalid'/delete/")
        self.assertEqual(response.status_code, 400)

    def test_delete_match_not_found(self):
        response = self.client.delete("/match/10/delete/")
        self.assertEqual(response.status_code, 400)
