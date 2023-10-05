from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from score.tests import generate_random_password

from .models import City, Ground, Tournament

# Create your tests here.

passwd = generate_random_password()
t_url = "/tour/tournament/"


class TournamentTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.com", password=passwd)
        self.client_t = APIClient()
        self.client_t.force_authenticate(user=self.user)
        self.city_tour = City.objects.create(name="Kottayam")
        self.ground_tour = Ground.objects.create(name="school")

        self.tournament_mt = Tournament.objects.create(
            id=1,
            name="Tournament_1",
            city=self.city_tour,
            ground=self.ground_tour,
            start_date="2023-09-20",
            end_date="2023-10-30",
            tournament_type=0,
            match_type=0,
            ball_type=0,
            user=self.user,
        )

    def test_tournament_list(self):
        response = self.client_t.get(t_url)
        print("1:", response.data)
        self.assertEqual(response.status_code, 200)

    def test_create_tournament_validation(self):
        response = self.client_t.post(
            t_url,
            {
                "name": "Tournament_test",
                "city": "abc",
                "ground": "g_abc",
                "start_date": "2023-07-21",
                "end_date": "2023-10-26",
                "tournament_type": 0,
                "match_type": 0,
                "ball_type": 0,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        response_1 = self.client_t.post(
            t_url,
            {
                "name": "Tournament_test",
                "city": "",
                "ground": "g_abc",
                "start_date": "2023-09-21",
                "end_date": "2023-10-26",
                "tournament_type": 0,
                "match_type": 0,
                "ball_type": 0,
            },
            format="json",
        )
        self.assertEqual(response_1.status_code, 400)

    def test_update_tournament(self):
        response = self.client_t.put(
            f"{t_url}?id=1",
            {
                "name": "",
                "city": "abcd",
                "ground": "g_abcd",
                "start_date": "2023-09-20",
                "end_date": "2023-10-25",
                "tournament_type": 0,
                "match_type": 0,
                "ball_type": 0,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        response_1 = self.client_t.put(
            f"{t_url}?id=1",
            {},
            format="json",
        )
        self.assertEqual(response_1.status_code, 400)

    def test_tournament_details(self):
        response = self.client_t.get(f"/tour/home/{self.tournament_mt.id}")
        response2 = self.client_t.get("/tour/home/500")
        response3 = self.client_t.get("/tour/home/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response2.status_code, 404)

    def test_ground_list(self):
        response = self.client_t.get("/tour/ground/")
        self.assertEqual(response.status_code, 200)

    def test_delete_tournament(self):
        response = self.client_t.put(
            "/tour/tournamentDelete/",
            {
                "tournament_id": 1,
                "deleted_reason": "abcd",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)

    def test_public_teams(self):
        response = self.client_t.get(f"/tour/{self.tournament_mt.id}/teams/")
        self.assertEqual(response.status_code, 200)
        response = self.client_t.get("/tour/invalid/teams/")
        self.assertEqual(response.status_code, 400)
