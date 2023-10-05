from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from score.tests import generate_random_password
from team.models import Team
from tournament.models import City, Ground, Tournament

from .models import TeamTournaments

# Create your tests here.
email_1 = "test@gmail.com"
passwd = generate_random_password()


class TestTeamTournament(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email=email_1, password=passwd)
        self.city_tm = City.objects.create(name="Kottayam")
        self.ground_tm = Ground.objects.create(name="school")
        self.tournament_tm = Tournament.objects.create(
            id=1,
            name="Tournament_1",
            city=self.city_tm,
            ground=self.ground_tm,
            start_date="2023-09-20",
            end_date="2023-10-30",
            tournament_type=0,
            match_type=0,
            ball_type=0,
            user=self.user,
        )
        self.team_tm = Team.objects.create(
            name="TestTeam", user=self.user, city=self.city_tm
        )
        self.team1_tm = Team.objects.create(
            name="TestTeam1", user=self.user, city=self.city_tm
        )
        self.team_tournament_gs4 = TeamTournaments.objects.create(
            tournament_id=self.tournament_tm, team_id=self.team_tm
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_addTeamToTournament(self):
        response = self.client.post(
            reverse("addTeamtoTournament"),
            {
                "tournament_id": 1,
                "team_id": self.team1_tm.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        response_1 = self.client.post(
            reverse("addTeamtoTournament"),
            {
                "tournament_id": 500,
                "team_id": self.team_tm.id,
            },
            format="json",
        )
        self.assertEqual(response_1.status_code, 400)

    def test_removeTeamFromTournament(self):
        response = self.client.put(
            reverse("removeTeamFromTournament"),
            {
                "tournament_id": 1,
                "team_id": self.team_tm.id,
            },
            format="json",
        )
        print("team_tour 69 : ", response.data)
        self.assertEqual(response.status_code, 200)
        response = self.client.put(
            reverse("removeTeamFromTournament"),
            {
                "tournament_id": 1,
                "team_id": self.team1_tm.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        response_1 = self.client.put(
            reverse("removeTeamFromTournament"),
            {
                "tournament_id": 1,
                "team_id": 500,
            },
            format="json",
        )
        self.assertEqual(response_1.status_code, 400)
