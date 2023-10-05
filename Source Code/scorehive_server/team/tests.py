from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase

from accounts.models import User
from score.tests import generate_random_password
from team.serializer import CitySerializer

from .models import City, Team
from .views import CityView

passwd = generate_random_password()
team_1 = "Team 1"
team_url = "/team/teams/"
updated = "Team 1 Updated"


class CityViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="gishwin.antony",
            password=passwd,
            name="jsdgj",
            phone_number="+911 7736415452",
        )
        self.city1 = City.objects.create(name="City 1")
        self.city2 = City.objects.create(name="City 2")

    def test_get_cities_unauthenticated(self):
        CityView.permission_classes = [IsAuthenticated]
        response = self.client.get("/team/cities/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_cities(self):
        CityView.permission_classes = []
        response = self.client.get("/team/cities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the response data
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_team(self):
        self.client.force_authenticate(user=self.user)
        self.team1 = Team.objects.create(name=team_1, user=self.user, city=self.city2)
        self.team2 = Team.objects.create(name="Team 2", user=self.user, city=self.city2)
        response = self.client.get(team_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_team_empty_table(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(team_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error = {"message": "Teams not found", "error_code": "4012"}
        self.assertEqual(response.data, error)

    def test_get_team_invalid_query(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/team/teams/?id=4")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = {
            "message": "Invalid query parameter. Only 'page' is allowed.",
            "error_code": 4011,
        }
        self.assertEqual(response.data, error)

    def test_get_team_invalid_page(self):
        self.client.force_authenticate(user=self.user)
        self.team1 = Team.objects.create(name=team_1, user=self.user, city=self.city2)
        self.team2 = Team.objects.create(name="Team 2", user=self.user, city=self.city2)
        response = self.client.get("/team/teams/?page=4")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = {"message": "Invalid page.", "error_code": 4013}
        self.assertEqual(response.data, error)

    def test_post_team_without_logo(self):
        self.client.force_authenticate(user=self.user)
        payload_data = {"name": team_1, "city": self.city1.id}
        response = self.client.post(team_url, payload_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_team_with_logo(self):
        self.client.force_authenticate(user=self.user)
        image_content = b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01\x01\x01\x00\x48\x00\x48\x00\x00\xff\xfe\x00\x13"
        image = SimpleUploadedFile(
            "sample_image.jpg", image_content, content_type="image/jpeg"
        )
        payload_data = {"name": team_1, "city": self.city1.id, "logo_url": image}
        response = self.client.post(team_url, payload_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_team_empty_logo(self):
        self.client.force_authenticate(user=self.user)
        payload_data = {"name": team_1, "city": self.city1.id, "logo_url": ""}
        response = self.client.post(team_url, payload_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = {"message": "Please insert an image", "error_code": 4006}
        self.assertEqual(response.data, error)

    def test_post_team_empty_data(self):
        self.client.force_authenticate(user=self.user)
        payload_data = {
            "name": "",
            "city": "",
        }
        response = self.client.post(team_url, payload_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_team_invalid_city1(self):
        self.client.force_authenticate(user=self.user)
        payload_data = {
            "name": team_1,
            "city": 1000,
        }
        response = self.client.post(team_url, payload_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = {"message": "City with this id is not available", "error_code": 4007}
        self.assertEqual(response.data, error)

    def test_post_team_invalid_city2(self):
        self.client.force_authenticate(user=self.user)
        payload_data = {
            "name": team_1,
            "city": "zdfdsgs",
        }
        response = self.client.post(team_url, payload_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = {"error_code": 4005, "message": "city must be an Integer"}
        self.assertEqual(response.data, error)

    def test_put_team(self):
        self.client.force_authenticate(user=self.user)
        self.team1 = Team.objects.create(name=team_1, user=self.user, city=self.city2)
        payload_data = {"name": updated, "city": self.city1.id}
        url = f"/team/teams/?id={self.team1.id}"
        response = self.client.put(url, data=payload_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_team_remove_logo(self):
        self.client.force_authenticate(user=self.user)
        self.team1 = Team.objects.create(name=team_1, user=self.user, city=self.city2)
        payload_data = {"name": updated, "city": self.city1.id, "logo_url": 1}
        url = f"/team/teams/?id={self.team1.id}"
        response = self.client.put(url, data=payload_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_team_invalid_id(self):
        self.client.force_authenticate(user=self.user)
        self.team1 = Team.objects.create(name=team_1, user=self.user, city=self.city2)
        payload_data = {
            "name": updated,
            "city": self.city1.id,
        }
        url = "/team/teams/?id=10000"
        response = self.client.put(url, data=payload_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error = {"message": "Team not found", "error_code": "4012"}
        self.assertEqual(response.data, error)

    def test_put_team_empty_data(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": "",
            "city": "",
        }
        response = self.client.post(team_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_team_invalid_city2(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "name": team_1,
            "city": "zdfdsgs",
        }
        response = self.client.post(team_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = {"error_code": 4005, "message": "city must be an Integer"}
        self.assertEqual(response.data, error)

    def test_delete_team(self):
        self.client.force_authenticate(user=self.user)
        self.team1 = Team.objects.create(name=team_1, user=self.user, city=self.city2)
        url = f"/team/teams/?id={self.team1.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message = {"message": "Successfully deleted"}
        self.assertEqual(response.data, message)

    def test_delete_team_invalid_id(self):
        self.client.force_authenticate(user=self.user)
        url = "/team/teams/?id=10000"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error = {"message": "Team not found", "error_code": "4012"}
        self.assertEqual(response.data, error)
