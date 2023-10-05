import secrets
import string

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from round.models import Round
from score.tests import generate_random_password
from scorehive_server.common import custom_errors
from team.models import City, Team
from team_tournaments.models import TeamTournaments
from tournament.models import Ground, Tournament

from .models import TournamentGroups, TournamentGroupTeams

email = "test@gmail.com"
email1 = "test1@gmail.com"
password1 = generate_random_password()
password2 = generate_random_password()
city_name = "Kottayam"
group_name = "Group 1"
group_2 = "Group 2"
groups_1 = "Groups 1"


class CreateGroup(APITestCase):
    def setUp(self):
        self.user_gs1 = User.objects.create(email=email, password=password1)
        self.user1_gs1 = User.objects.create(email=email1, password=password2)
        self.city_gs1 = City.objects.create(name=city_name)
        self.ground_gs1 = Ground.objects.create(name="school")
        self.round_gs1 = Round.objects.create(id=1, name="round1", round_type=1)
        self.team_gs1 = Team.objects.create(
            name="TestTeam", user=self.user_gs1, city=self.city_gs1
        )
        self.team1_gs1 = Team.objects.create(
            name="TestTeam1", user=self.user_gs1, city=self.city_gs1
        )
        self.tournament_gs1 = Tournament.objects.create(
            name="Tournament_1",
            city=self.city_gs1,
            ground=self.ground_gs1,
            start_date="2023-07-20",
            end_date="2023-07-25",
            tournament_type=0,
            match_type=0,
            ball_type=0,
            user=self.user_gs1,
        )
        self.tournament1_gs1 = Tournament.objects.create(
            name="Tournament_2",
            city=self.city_gs1,
            ground=self.ground_gs1,
            start_date="2023-07-20",
            end_date="2023-07-25",
            tournament_type=0,
            match_type=0,
            ball_type=0,
            user=self.user1_gs1,
        )
        self.team_tournament_gs1 = TeamTournaments.objects.create(
            tournament_id=self.tournament1_gs1, team_id=self.team_gs1
        )
        self.tournament_team_gs1 = TeamTournaments.objects.create(
            tournament_id=self.tournament_gs1, team_id=self.team_gs1
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_gs1)

    def test_missing_keys(self):
        response = self.client.post(reverse("createGroup"), {}, format="json")
        self.assertEqual(response.data, custom_errors.MISSING_REQUIRED_FIELDS)

    def test_invalid_tournament_id(self):
        response = self.client.post(
            reverse("createGroup"),
            {"tournament_id": "invalid", "name": group_2, "team_ids": [1]},
            format="json",
        )
        self.assertEqual(response.data, custom_errors.ERR_1038)
        self.assertEqual(response.status_code, 400)

    def test_invalid_team_ids(self):
        response = self.client.post(
            reverse("createGroup"),
            {"tournament_id": 1, "name": group_2, "team_ids": "invalid"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_tournament_not_created_by_current_user(self):
        response = self.client.post(
            reverse("createGroup"),
            {"tournament_id": 2, "name": group_2, "team_ids": [1]},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_teams_not_in_tournament(self):
        response = self.client.post(
            reverse("createGroup"),
            {"tournament_id": self.tournament_gs1.id, "name": group_2, "team_ids": [5]},
            format="json",
        )
        self.assertEqual(
            response.data,
            {
                "error_code": 1055,
                "message": "Some teams are not in this tournament",
                "team_ids_not_in_tournament": [5],
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_with_valid_data(self):
        response = self.client.post(
            reverse("createGroup"),
            {
                "tournament_id": self.tournament_gs1.id,
                "name": group_name,
                "team_ids": [self.team_gs1.id],
            },
            format="json",
        )
        self.assertEqual(response.data, {"message": "Group added"})
        self.assertEqual(response.status_code, 200)

        # Test for serializer error
        response = self.client.post(
            reverse("createGroup"),
            {
                "tournament_id": self.tournament_gs1.id,
                "name": "G",
                "team_ids": [self.team_gs1.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        response = self.client.post(
            reverse("createGroup"),
            {
                "tournament_id": self.tournament_gs1.id,
                "name": group_name,
                "team_ids": [self.team_gs1.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            reverse("createGroup"),
            {
                "tournament_id": self.tournament_gs1.id,
                "name": "Group Team test",
                "team_ids": [self.team_gs1.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)


class ListGroup(APITestCase):
    def setUp(self):
        self.user_gs2 = User.objects.create(email=email, password=password1)
        self.user1_gs2 = User.objects.create(email=email1, password=password2)
        self.city_gs2 = City.objects.create(name=city_name)
        self.ground_gs2 = Ground.objects.create(name="school")
        self.round_gs2 = Round.objects.create(id=1, name="round1", round_type=1)
        self.team_gs2 = Team.objects.create(
            name="TestTeam", user=self.user_gs2, city=self.city_gs2
        )
        self.tournament_gs2 = Tournament.objects.create(
            name="Tournament_1_gs2",
            city=self.city_gs2,
            ground=self.ground_gs2,
            start_date="2023-07-20",
            end_date="2023-07-25",
            tournament_type=0,
            match_type=0,
            ball_type=1,
            user=self.user_gs2,
        )
        self.tournament1_gs2 = Tournament.objects.create(
            name="Tournament_2_gs2",
            city=self.city_gs2,
            ground=self.ground_gs2,
            start_date="2023-07-20",
            end_date="2023-07-25",
            tournament_type=0,
            match_type=1,
            ball_type=0,
            user=self.user_gs2,
        )
        self.team_tournament_gs2 = TeamTournaments.objects.create(
            tournament_id=self.tournament1_gs2, team_id=self.team_gs2
        )
        self.tournament_team_gs2 = TeamTournaments.objects.create(
            tournament_id=self.tournament_gs2, team_id=self.team_gs2
        )
        self.group_gs2 = TournamentGroups.objects.create(
            id=1,
            name="Group_1",
            tournament_id=self.tournament1_gs2,
            round_id=self.round_gs2,
        )
        self.groupTeam_gs2 = TournamentGroupTeams.objects.create(
            group_id=self.group_gs2, team_id=self.team_gs2
        )
        self.client_gs2 = APIClient()
        self.client_gs2.force_authenticate(user=self.user_gs2)

    def test_invalid_tournament_id(self):
        response = self.client_gs2.get("/group/invalid_id/listGroup/")
        self.assertEqual(response.data, custom_errors.ERR_1038)
        self.assertEqual(response.status_code, 400)

    def test_valid_tournament_with_no_group(self):
        response = self.client_gs2.get(f"/group/{self.tournament_gs2.id}/listGroup/")
        self.assertEqual(response.data, custom_errors.ERR_4014)
        self.assertEqual(response.status_code, 400)

    def test_valid_tournament_with_group(self):
        response = self.client_gs2.get(f"/group/{self.tournament1_gs2.id}/listGroup/")
        self.assertEqual(response.status_code, 200)


class UngroupedTeams(APITestCase):
    def setUp(self):
        self.user_gs3 = User.objects.create(email=email, password=password1)
        self.user1_gs3 = User.objects.create(email=email1, password=password2)
        self.city_gs3 = City.objects.create(name=city_name)
        self.ground_gs3 = Ground.objects.create(name="school")
        self.round_gs3 = Round.objects.create(id=1, name="round1", round_type=1)
        self.team1_gs3 = Team.objects.create(
            name="TestTeam", user=self.user_gs3, city=self.city_gs3
        )
        self.team2_gs3 = Team.objects.create(
            name="TestTeam2", user=self.user_gs3, city=self.city_gs3
        )
        self.tournament_gs3 = Tournament.objects.create(
            name="Tournament_1",
            city=self.city_gs3,
            ground=self.ground_gs3,
            start_date="2023-07-20",
            end_date="2023-07-25",
            tournament_type=1,
            match_type=0,
            ball_type=0,
            user=self.user_gs3,
        )
        self.tournament2_gs3 = Tournament.objects.create(
            name="Tournament_1",
            city=self.city_gs3,
            ground=self.ground_gs3,
            start_date="2023-07-20",
            end_date="2023-07-25",
            tournament_type=0,
            match_type=0,
            ball_type=0,
            user=self.user1_gs3,
        )
        self.tournament_team_1_gs3 = TeamTournaments.objects.create(
            tournament_id=self.tournament_gs3, team_id=self.team1_gs3
        )
        self.tournament_team_2_gs3 = TeamTournaments.objects.create(
            tournament_id=self.tournament_gs3, team_id=self.team2_gs3
        )
        self.group_gs3 = TournamentGroups.objects.create(
            id=1,
            name="Group_1",
            tournament_id=self.tournament_gs3,
            round_id=self.round_gs3,
        )
        self.groupTeam_gs3 = TournamentGroupTeams.objects.create(
            group_id=self.group_gs3, team_id=self.team1_gs3
        )
        self.client_gs3 = APIClient()
        self.client_gs3.force_authenticate(user=self.user_gs3)

    def test_valid_tournament_ungrouped(self):
        response = self.client_gs3.get(f"/group/{self.tournament_gs3.id}/listTeam/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_tournament_id(self):
        response = self.client_gs3.get("/group/invalid_id/listTeam/")
        self.assertEqual(response.data, custom_errors.ERR_1038)
        self.assertEqual(response.status_code, 400)

    def test_tournament_not_created_by_current_user(self):
        response = self.client_gs3.get(f"/group/{self.tournament2_gs3.id}/listTeam/")
        self.assertEqual(response.data, custom_errors.ERR_1039)
        self.assertEqual(response.status_code, 400)


class UpdateGroup(APITestCase):
    def setUp(self):
        self.user_gs4 = User.objects.create(email=email, password=password1)
        self.user1_gs4 = User.objects.create(email=email1, password=password2)
        self.city_gs4 = City.objects.create(name=city_name)
        self.ground_gs4 = Ground.objects.create(name="school")
        self.round_gs4 = Round.objects.create(id=1, name="round1", round_type=1)
        self.team_gs4 = Team.objects.create(
            name="TestTeam", user=self.user_gs4, city=self.city_gs4
        )
        self.team1_gs4 = Team.objects.create(
            name="TestTeam1", user=self.user_gs4, city=self.city_gs4
        )
        self.team2_gs4 = Team.objects.create(
            name="TestTeam2", user=self.user_gs4, city=self.city_gs4
        )
        self.tournament_gs4 = Tournament.objects.create(
            name="Tournament_1",
            city=self.city_gs4,
            ground=self.ground_gs4,
            start_date="2023-08-20",
            end_date="2023-10-25",
            tournament_type=0,
            match_type=0,
            ball_type=0,
            user=self.user_gs4,
        )
        self.tournament1_gs4 = Tournament.objects.create(
            name="Tournament_2",
            city=self.city_gs4,
            ground=self.ground_gs4,
            start_date="2023-08-20",
            end_date="2023-08-25",
            tournament_type=0,
            match_type=1,
            ball_type=1,
            user=self.user1_gs4,
        )
        self.team_tournament_gs4 = TeamTournaments.objects.create(
            tournament_id=self.tournament1_gs4, team_id=self.team_gs4
        )
        self.tournament_team_gs4 = TeamTournaments.objects.create(
            tournament_id=self.tournament_gs4, team_id=self.team_gs4
        )
        self.tournament_team_gs4 = TeamTournaments.objects.create(
            tournament_id=self.tournament_gs4, team_id=self.team2_gs4
        )
        self.tournament_groups_gs4 = TournamentGroups.objects.create(
            id=1,
            name=group_name,
            tournament_id=self.tournament_gs4,
            round_id=self.round_gs4,
        )
        self.tournament_groups1_gs4 = TournamentGroups.objects.create(
            id=100,
            name=groups_1,
            tournament_id=self.tournament_gs4,
            round_id=self.round_gs4,
        )
        self.tournament_group_team1_gs4 = TournamentGroupTeams.objects.create(
            group_id=self.tournament_groups_gs4, team_id=self.team_gs4
        )
        self.client_gs4 = APIClient()
        self.client_gs4.force_authenticate(user=self.user_gs4)

    def test_missing_keys(self):
        response = self.client_gs4.put(reverse("updateGroup"), {}, format="json")
        self.assertEqual(response.data, custom_errors.MISSING_REQUIRED_FIELDS)

    def test_invalid_tournament_id(self):
        response = self.client_gs4.put(
            reverse("updateGroup"),
            {
                "group_id": 1,
                "tournament_id": "invalid",
                "name": group_2,
                "team_ids": [1],
            },
            format="json",
        )
        self.assertEqual(response.data, custom_errors.ERR_1038)
        self.assertEqual(response.status_code, 400)

    def test_invalid_team_ids(self):
        response = self.client_gs4.put(
            reverse("updateGroup"),
            {
                "group_id": 1,
                "tournament_id": 1,
                "name": group_2,
                "team_ids": "invalid",
            },
            format="json",
        )
        self.assertEqual(response.data, custom_errors.ERR_1057)
        self.assertEqual(response.status_code, 400)

    def test_tournament_not_created_by_current_user(self):
        response = self.client_gs4.put(
            reverse("updateGroup"),
            {"group_id": 1, "tournament_id": 2, "name": group_2, "team_ids": [1]},
            format="json",
        )
        self.assertEqual(response.data, custom_errors.ERR_1039)
        self.assertEqual(response.status_code, 400)

    def test_teams_not_in_tournament(self):
        response = self.client_gs4.put(
            reverse("updateGroup"),
            {
                "group_id": 1,
                "tournament_id": self.tournament_gs4.id,
                "name": group_2,
                "team_ids": [5],
            },
            format="json",
        )
        self.assertEqual(
            response.data,
            {
                "error_code": 1055,
                "message": "Some teams are not in this tournament",
                "team_ids_not_in_tournament": [5],
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_with_existing_name(self):
        response = self.client_gs4.put(
            reverse("updateGroup"),
            {
                "group_id": 1,
                "tournament_id": self.tournament_gs4.id,
                "name": groups_1,
                "team_ids": [self.team_gs4.id],
            },
            format="json",
        )
        self.assertEqual(
            response.data,
            {"error_code": 1056, "message": "Group already exists with this name"},
        )
        self.assertEqual(response.status_code, 400)

    def test_with_valid_data(self):
        response = self.client_gs4.put(
            reverse("updateGroup"),
            {
                "group_id": 1,
                "tournament_id": self.tournament_gs4.id,
                "name": group_2,
                "team_ids": [self.team2_gs4.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        response = self.client_gs4.put(
            reverse("updateGroup"),
            {
                "group_id": 1,
                "tournament_id": self.tournament_gs4.id,
                "name": group_2,
                "team_ids": [self.team_gs4.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)


class DeleteGroup(UpdateGroup):
    def test_missing_keys(self):
        response = self.client_gs4.put(reverse("deleteGroup"), {}, format="json")
        self.assertEqual(response.data, custom_errors.MISSING_REQUIRED_FIELDS)

    def test_group_not_found(self):
        response = self.client_gs4.put(
            reverse("deleteGroup"),
            {
                "tournament_id": self.tournament_gs4.id,
                "group_id": 10,
            },
            format="json",
        )
        self.assertEqual(response.data, custom_errors.ERR_4014)

    def test_invalid_tournament_id(self):
        response = self.client_gs4.put(
            reverse("deleteGroup"),
            {
                "group_id": 1,
                "tournament_id": "invalid",
            },
            format="json",
        )
        self.assertEqual(response.data, custom_errors.ERR_1038)
        self.assertEqual(response.status_code, 400)

    def test_valid_data(self):
        response = self.client_gs4.put(
            reverse("deleteGroup"),
            {
                "tournament_id": self.tournament_gs4.id,
                "group_id": self.tournament_groups_gs4.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)


class GroupDetail(APITestCase):
    def setUp(self):
        self.user_gs5 = User.objects.create(email=email, password=password1)
        self.user1_gs5 = User.objects.create(email=email1, password=password2)
        self.city_gs5 = City.objects.create(name=city_name)
        self.ground_gs5 = Ground.objects.create(name="school")
        self.round_gs5 = Round.objects.create(id=1, name="round1", round_type=1)
        self.team_gs5 = Team.objects.create(
            name="TestTeam", user=self.user_gs5, city=self.city_gs5
        )
        self.team1_gs5 = Team.objects.create(
            name="TestTeam1", user=self.user_gs5, city=self.city_gs5
        )
        self.team2_gs5 = Team.objects.create(
            name="TestTeam2", user=self.user_gs5, city=self.city_gs5
        )
        self.tournament_gs5 = Tournament.objects.create(
            name="Tournament_1",
            city=self.city_gs5,
            ground=self.ground_gs5,
            start_date="2023-08-20",
            end_date="2023-08-25",
            tournament_type=1,
            match_type=1,
            ball_type=1,
            user=self.user_gs5,
        )
        self.tournament1_gs5 = Tournament.objects.create(
            name="Tournament_2",
            city=self.city_gs5,
            ground=self.ground_gs5,
            start_date="2023-08-20",
            end_date="2023-08-25",
            tournament_type=1,
            match_type=1,
            ball_type=0,
            user=self.user1_gs5,
        )
        self.team_tournament_gs5 = TeamTournaments.objects.create(
            tournament_id=self.tournament1_gs5, team_id=self.team_gs5
        )
        self.tournament_team1_gs5 = TeamTournaments.objects.create(
            tournament_id=self.tournament_gs5, team_id=self.team_gs5
        )
        self.tournament_team2 = TeamTournaments.objects.create(
            tournament_id=self.tournament_gs5, team_id=self.team2_gs5
        )
        self.tournament_groups_gs5 = TournamentGroups.objects.create(
            id=1,
            name=group_name,
            tournament_id=self.tournament_gs5,
            round_id=self.round_gs5,
        )
        self.tournament_groups1_gs5 = TournamentGroups.objects.create(
            id=100,
            name=groups_1,
            tournament_id=self.tournament_gs5,
            round_id=self.round_gs5,
        )
        self.tournament_group_team1_gs5 = TournamentGroupTeams.objects.create(
            group_id=self.tournament_groups_gs5, team_id=self.team_gs5
        )
        self.client_gs5 = APIClient()
        self.client_gs5.force_authenticate(user=self.user_gs5)

    def test_valid_request(self):
        response = self.client_gs5.get(
            f"/group/details/{self.tournament_groups_gs5.id}/"
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_group_id(self):
        response = self.client_gs5.get("/group/details/invalid/")
        self.assertEqual(response.data, custom_errors.ERR_1059)
        response = self.client_gs5.get("/group/details/-1/")
        self.assertEqual(response.data, custom_errors.ERR_1059)

    def test_group_not_found(self):
        response = self.client_gs5.get("/group/details/500/")
        self.assertEqual(response.data, custom_errors.ERR_1063)
