import secrets
import string

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from group.models import TournamentGroups, TournamentGroupTeams
from match.models import Ground, Matches, Tournament
from round.models import Round, TournamentRounds
from team.models import City, Team
from team_players.models import TeamPlayers
from team_tournaments.models import TeamTournaments


# Create your tests here.
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation

    password = "".join(secrets.choice(characters) for i in range(length))

    return password


passwd1 = generate_random_password()
passwd2 = generate_random_password()
passwd3 = generate_random_password()


class Score(APITestCase):
    def setUp(self):
        self.user_st = User.objects.create(
            id=1, email="test@mail.com", password=passwd1
        )
        self.user1_st = User.objects.create(
            id=2, email="test1@mail.com", password=passwd2
        )
        self.user2_st = User.objects.create(
            id=3, email="test2@mail.com", password=passwd3
        )
        self.city_st = City.objects.create(name="Kottayam")
        self.ground_st = Ground.objects.create(name="school")
        self.round_st = Round.objects.create(id=1, name="round1", round_type=1)
        self.team_st = Team.objects.create(
            name="TestTeam", user=self.user_st, city=self.city_st
        )
        self.team1_st = Team.objects.create(
            name="TestTeam1", user=self.user_st, city=self.city_st
        )
        self.tournament_st = Tournament.objects.create(
            name="Tournament_1",
            city=self.city_st,
            ground=self.ground_st,
            start_date="2023-08-20",
            end_date="2023-08-30",
            tournament_type=0,
            match_type=1,
            ball_type=0,
            user=self.user_st,
        )

        self.tournament_team_st = TeamTournaments.objects.create(
            tournament_id=self.tournament_st, team_id=self.team_st
        )
        self.tournament_team2_st = TeamTournaments.objects.create(
            tournament_id=self.tournament_st, team_id=self.team1_st
        )
        self.group_st = TournamentGroups.objects.create(
            name="Group", tournament_id=self.tournament_st
        )
        self.group_team1_st = TournamentGroupTeams.objects.create(
            group_id=self.group_st, team_id=self.team_st
        )
        self.group_team2_st = TournamentGroupTeams.objects.create(
            group_id=self.group_st, team_id=self.team1_st
        )
        self.round1_st = Round.objects.create(name="Round 1")
        self.round2_st = Round.objects.create(name="Round 2")
        self.tournament_round_1_st = TournamentRounds.objects.create(
            tournament_id=self.tournament_st, round_id=self.round1_st
        )
        self.tournament_round_2_st = TournamentRounds.objects.create(
            tournament_id=self.tournament_st, round_id=self.round2_st
        )
        self.match_st = Matches.objects.create(
            tournament_id=self.tournament_st,
            team1=self.team1_st,
            team2=self.team_st,
            match_type=1,
            date_time="2023-08-24T09:50",
            round_id=self.round2_st,
            city_id=self.city_st,
            ground_id=self.ground_st,
            over_per_bowler=2,
            total_overs=6,
            ball_type=self.tournament_st.ball_type,
        )
        self.team_player1_st = TeamPlayers.objects.create(
            team_id=self.team_st, player_id=self.user_st
        )
        self.team_player2_st = TeamPlayers.objects.create(
            team_id=self.team_st, player_id=self.user1_st
        )
        self.team_player3 = TeamPlayers.objects.create(
            team_id=self.team1_st, player_id=self.user2_st
        )

        self.client_st = APIClient()
        self.client_st.force_authenticate(user=self.user_st)

    def test_score_with_valid_data(self):
        response = self.client_st.post(
            reverse("addScore"),
            [
                {
                    "match_id": self.match_st.id,
                    "inning": 1,
                    "batting_team": self.team_st.id,
                    "over": 1,
                    "ball_number": 1,
                    "striker_id": self.user_st.id,
                    "non_striker_id": self.user1_st.id,
                    "bowler_id": 3,
                    "runs": 1,
                    "is_wicket": 0,
                },
            ],
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_score_with_invalid_data(self):
        response = self.client_st.post(
            reverse("addScore"),
            [
                {
                    "match_id": self.match_st.id,
                    "inning": 1,
                    "batting_team": self.team_st.id,
                    "over": 1,
                    "ball_number": 1,
                    "striker_id": self.user_st.id,
                    "non_striker_id": self.user_st.id,
                    "bowler_id": 3,
                    "runs": 1,
                    "is_wicket": 0,
                },
            ],
            format="json",
        )
        self.assertEqual(response.status_code, 400)
