from unittest.mock import patch

from django.core.mail import EmailMessage
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from score.tests import generate_random_password
from team.models import City, Team
from team_players.models import TeamPlayers

# Create your tests here.
passwd = generate_random_password()
email = "test@gmail.com"
email2 = "test2@gmail.com"
positive_team_id = "team_id should be a positive integer"
not_found = "Team not found"


class TestPlayerListAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email=email, password=passwd)

        self.city = City.objects.create(name="Kottayam")
        self.team = Team.objects.create(name="TestTeam", user=self.user, city=self.city)
        self.team_player = TeamPlayers.objects.create(
            team_id=self.team, player_id=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_non_integer_team_id(self):
        response = self.client.get(reverse("playerList", kwargs={"teamid": "invalid"}))
        self.assertEqual(
            response.data,
            {"error_code": 4015, "message": positive_team_id},
        )

    def test_non_existing_team(self):
        response = self.client.get(reverse("playerList", kwargs={"teamid": "500"}))
        self.assertEqual(response.data, {"error_code": 4012, "message": not_found})

    @patch("team_players.models.Team.objects.get")
    def test_other_exceptions(self, mock_get):
        mock_get.side_effect = Exception("Get method failed")
        response = self.client.get(
            reverse("playerList", kwargs={"teamid": self.team.id})
        )
        self.assertEqual(response.status_code, 400)

    def test_player_list_success(self):
        response = self.client.get(
            reverse("playerList", kwargs={"teamid": self.team.id})
        )
        self.assertEqual(response.status_code, 200)


class TestSearchPlayerAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email=email, password=passwd)
        self.user2 = User.objects.create(email="tests@gmail.com", password=passwd)
        self.city = City.objects.create(name="Kottayam")
        self.team = Team.objects.create(name="TestTeam", user=self.user, city=self.city)
        self.team_player = TeamPlayers.objects.create(
            team_id=self.team, player_id=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_email_required_field(self):
        response = self.client.post(reverse("searchPlayer"), {}, format="json")
        self.assertEqual(
            response.data, {"error_code": 1001, "message": "All fields are required"}
        )

    def test_user_non_existing(self):
        response = self.client.post(
            reverse("searchPlayer"),
            {"email": email2, "team_id": self.team.id},
            format="json",
        )
        self.assertEqual(
            response.data,
            {
                "error_code": 1043,
                "message": "No email matching the search",
            },
        )

    def test_email_length(self):
        response = self.client.post(
            reverse("searchPlayer"),
            {
                "email": "testsjhfdkgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggghsduyuyvsdfvsdfvjdfvyr"
                "ehbfjsdbvduvggggggggggggggggggggggggggggggggggg@gmail.com",
                "team_id": self.team.id,
            },
            format="json",
        )
        self.assertEqual(
            response.data,
            {
                "error_code": 1003,
                "message": "Maximum length of email should be 100 characters",
            },
        )

    @patch("accounts.models.User.objects.get")
    def test_other_exceptions(self, get_mock):
        get_mock.side_effect = Exception("Get method failed")
        response = self.client.post(
            reverse("searchPlayer"), {"email": email}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_search_player_success(self):
        response = self.client.post(
            reverse("searchPlayer"),
            {"email": "tests@gmail.com", "team_id": self.team.id},
            format="json",
        )
        self.assertEqual(response.status_code, 200)


class TestCheckPlayerTeamMember(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email=email, password=passwd)
        self.user2 = User.objects.create(email=email2, password=passwd)
        self.city = City.objects.create(name="Kottayam")
        self.team = Team.objects.create(name="TestTeam", user=self.user, city=self.city)
        self.team_player = TeamPlayers.objects.create(
            team_id=self.team, player_id=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_team_id_required_field(self):
        response = self.client.post(
            reverse("checkPlayerMemberOfTeam"), {}, format="json"
        )
        self.assertEqual(
            response.data, {"error_code": 1025, "message": "team_id is required"}
        )
        self.assertEqual(response.status_code, 400)

    def test_team_id_invalid(self):
        response = self.client.post(
            reverse("checkPlayerMemberOfTeam"), {"team_id": "invalid"}, format="json"
        )
        self.assertEqual(
            response.data,
            {"error_code": 4015, "message": positive_team_id},
        )

    def test_team_not_found(self):
        response = self.client.post(
            reverse("checkPlayerMemberOfTeam"), {"team_id": 10}, format="json"
        )
        self.assertEqual(response.data, {"error_code": 4012, "message": not_found})

    def test_player_already_member(self):
        response = self.client.post(
            reverse("checkPlayerMemberOfTeam"), {"team_id": self.team.id}, format="json"
        )
        self.assertEqual(
            response.data,
            {"error_code": 1027, "message": "User is already member of the team"},
        )

    def test_player_not_member(self):
        client = APIClient()
        client.force_authenticate(user=self.user2)
        response = client.post(
            reverse("checkPlayerMemberOfTeam"), {"team_id": self.team.id}, format="json"
        )
        self.assertEqual(response.data, {"message": "Player not member of team"})


class TestPlayerJoinToTeam(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email=email, password=passwd)
        self.user2 = User.objects.create(email=email2, password=passwd)
        self.city = City.objects.create(name="Kottayam")
        self.team = Team.objects.create(name="TestTeam", user=self.user, city=self.city)
        self.team_player = TeamPlayers.objects.create(
            team_id=self.team, player_id=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_team_id_required_field(self):
        response = self.client.post(reverse("playerJoinToTeam"), {}, format="json")
        self.assertEqual(
            response.data, {"error_code": 1025, "message": "team_id is required"}
        )

    def test_team_id_invalid(self):
        response = self.client.post(
            reverse("playerJoinToTeam"), {"team_id": "invalid"}, format="json"
        )
        self.assertEqual(
            response.data,
            {"error_code": 4015, "message": "TeamId should be a positive integer"},
        )

    def test_team_not_found(self):
        response = self.client.post(
            reverse("playerJoinToTeam"), {"team_id": 10}, format="json"
        )
        self.assertEqual(response.data, {"error_code": 4012, "message": not_found})

    def test_player_already_member(self):
        response = self.client.post(
            reverse("playerJoinToTeam"), {"team_id": self.team.id}, format="json"
        )
        self.assertEqual(
            response.data,
            {"error_code": 1027, "message": "User is already member of the team"},
        )

    def test_player_join_to_team_success(self):
        client = APIClient()
        client.force_authenticate(self.user2)
        response = client.post(
            reverse("playerJoinToTeam"), {"team_id": self.team.id}, format="json"
        )
        self.assertEqual(response.data, {"message": "Player joined in team"})


class TestInvitePlayerToTeam(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email=email, password=passwd)
        self.city = City.objects.create(name="Kottayam")
        self.team = Team.objects.create(name="TestTeam", user=self.user, city=self.city)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_missing_required_fields(self):
        response = self.client.post(reverse("invitePlayerToTeam"), {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_team_id_invalid(self):
        response = self.client.post(
            reverse("invitePlayerToTeam"),
            {"email": self.user.email, "team_id": "invalid"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_already_existing_email(self):
        response = self.client.post(
            reverse("invitePlayerToTeam"),
            {"email": self.user.email, "team_id": self.team.id},
            format="json",
        )
        self.assertEqual(
            response.data,
            {"error_code": 2001, "message": "User with this email already exist"},
        )

    def test_email_length(self):
        response = self.client.post(
            reverse("invitePlayerToTeam"),
            {
                "email": "testsjhfdkgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggghsdu"
                "yuyvsdfvsdfvjdfvyrehbfjsdbvduvggggggggggggggggggggggggggggggggggg@gmail.com",
                "team_id": self.team.id,
            },
            format="json",
        )
        self.assertEqual(
            response.data,
            {
                "error_code": 1003,
                "message": "Maximum length of email should be 100 characters",
            },
        )

    def test_non_existing_team(self):
        response = self.client.post(
            reverse("invitePlayerToTeam"),
            {"email": email2, "team_id": 5},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        response = self.client.post(
            reverse("invitePlayerToTeam"),
            {"email": "testgmail.com", "team_id": self.team.id},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_negative_team_id(self):
        response = self.client.post(
            reverse("invitePlayerToTeam"),
            {"email": email2, "team_id": -5},
            format="json",
        )
        self.assertEqual(
            response.data,
            {"error_code": 4015, "message": positive_team_id},
        )

    @patch.object(EmailMessage, "send")
    def test_email_sending_failure(self, send_mock):
        send_mock.side_effect = Exception("Email sending failed")
        response = self.client.post(
            reverse("invitePlayerToTeam"),
            {"email": "abraham.jacob@innovaturelabs.com", "team_id": self.team.id},
            format="json",
        )
        self.assertEqual(
            response.data,
            {"error_code": 1029, "message": "Invitation link sending failed"},
        )

    def test_invite_to_team_success(self):
        response = self.client.post(
            reverse("invitePlayerToTeam"),
            {"email": email2, "team_id": self.team.id},
            format="json",
        )
        self.assertEqual(response.data, "Invitation sent")
