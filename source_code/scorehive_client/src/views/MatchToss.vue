<template>
  <NavBar />
  <div>
    <div class="d-flex justify-content-center">
      <div id="coin"></div>
      <div class="card shadow-lg mx-lg-5 my-lg-5 bg-white p-4 w-50">
        <div class="d-flex justify-content-between">
          <h4 class="text-dark">Who won the toss?</h4>
          <div></div>
        </div>
        <hr />
        <div class="row mt-sm-4 mx-lg-5 mx-sm-2">
          <divk
            v-for="(teams, index) in teams"
            :key="index"
            class="col-md-6 col-sm-4"
          >
            <div
              :class="{ 'selected-card': isSelected(teams.id) }"
              class="card shadow m-2 p-2"
              @click="toggleSelection(teams.id)"
            >
              <LogoContainer
                :showImage="teams.user_profile"
                class="d-flex justify-content-center m-1 mx-lg-4"
                borderRadius="50%"
                containerWidth="100"
                :imageUrl="teams.user_profile"
              />
              <p class="text-center">
                <b>{{ teams.name }}</b>
              </p>
            </div>
          </divk>
        </div>
        <br />
        <div class="d-flex justify-content-between">
          <h4 class="text-dark">Winner of the toss elected to</h4>
          <div></div>
        </div>
        <hr />
        <div class="row mt-sm-4 mx-lg-5 mx-sm-2">
          <div
            v-for="(category, index) in category"
            :key="index"
            class="col-md-6 col-sm-4"
          >
            <div
              class="card shadow m-2 p-2"
              :class="{ 'selected-card': isCategorySelected(category.id) }"
              @click="toggleCategorySelection(category.id)"
            >
              <LogoContainer
                :showImage="category.logo"
                class="d-flex justify-content-center m-1 mx-lg-4"
                borderRadius="50%"
                containerWidth="100"
                :imageUrl="category.logo"
              />
              <p class="text-center">
                <b>{{ category.name }}</b>
              </p>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="d-flex pt-4 mb-2">
            <cbutton
              class="btn btn-primary"
              type="button"
              color="primary"
              style="margin-left: 70px"
              @click="playGame()"
              ><span
                v-if="isLoading"
                class="spinner-border spinner-border-sm me-2"
                role="status"
                aria-hidden="true"
              ></span>
              <span v-else><span>Let's Play</span></span></cbutton
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import errorCodes from "@/services/errorCodes.json";
import LogoContainer from "@/components/LogoContainer.vue";
import Swal from "sweetalert2";
import cbutton from "@/components/Button.vue";
import NavBar from "./NavBar.vue";
import user_profile from "@/assets/img/logo1.jpg";
import logos from "@/assets/img/logo2.jpg";
import bating from "@/assets/img/batting.jpeg";
import bowling1 from "@/assets/img/boll.jpeg";
import { playerList } from "@/services/playerService";

export default {
  components: {
    NavBar,
    cbutton,
    LogoContainer,
  },
  data() {
    return {
      user_profile: user_profile,
      logos: logos,
      selectedcategoryCardId: null,
      bowling1: bowling1,
      bating: bating,
      selectedCardId: null,
      teams: [],
      category: [
        {
          id: 11,
          name: "BAT",
          logo: bating,
        },
        {
          id: 12,
          name: "BOWL",
          logo: bowling1,
        },
      ],
    };
  },
  mounted() {
    if (this.$route?.params?.MatchId) {
      const secret = "tournamentMatch";
      try {
        this.tournamentId = atob(this.$route?.params?.tournamentId).replace(
          secret,
          ""
        );
        this.MatchId = atob(this.$route?.params?.MatchId).replace(secret, "");
        this.team1 = atob(this.$route?.params?.team1).replace(secret, "");
        this.team2 = atob(this.$route?.params?.team2).replace(secret, "");
        this.team1Id = atob(this.$route?.params?.id1).replace(secret, "");
        this.team2Id = atob(this.$route?.params?.id2).replace(secret, "");
      } catch (error) {
        this.$router.push("not-found");
      }
    }
    this.displayTeams();
  },
  methods: {
    displayTeams() {
      this.teams = [
        {
          id: this.team1Id,
          name: this.team1,
          user_profile:
            "https://static.vecteezy.com/system/resources/previews/000/365/307/original/cricket-logo-vector.jpg",
        },
        {
          id: this.team2Id,
          name: this.team2,
          user_profile:
            "https://www.shutterstock.com/shutterstock/photos/2195238533/display_1500/stock-vector-cricket-logo-championship-with-player-illustration-vector-2195238533.jpg",
        },

        // Add more teams as needed
      ];
    },
    toggleSelection(team) {
      if (this.isSelected(team)) {
        // If the card is already selected, deselect it
        this.selectedCardId = null;
      } else {
        // If the card is not selected, set it as the selectedCardId
        this.selectedCardId = team;
      }
    },
    isSelected(team) {
      // Check if the card is selected by comparing with the selectedCardId

      return this.selectedCardId === team;
    },
    toggleCategorySelection(category) {
      if (this.isCategorySelected(category)) {
        // If the card is already selected, deselect it
        this.selectedcategoryCardId = null;
      } else {
        // If the card is not selected, set it as the selectedCardId
        this.selectedcategoryCardId = category;
      }
    },
    isCategorySelected(category) {
      // Check if the card is selected by comparing with the selectedCardId
      return this.selectedcategoryCardId === category;
    },
    playGame() {
      if (!this.selectedCardId || !this.selectedcategoryCardId) {
        // Show an error message if either team or category is not selected
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Please select both a team and a category (bat or bowl) before playing!",
        });
      } else {
        // Find the selected team and category based on the selected IDs
        const selectedTeam = this.teams.find(
          (team) => team.id === this.selectedCardId
        );
        const selectedCategory = this.category.find(
          (cat) => cat.id === this.selectedcategoryCardId
        );
        const nonSelectedTeam = this.teams.find(
          (team) => team.id !== this.selectedCardId
        );

        playerList(selectedTeam.id).then(
          (response) => {
            this.playerlist = response.data;
            this.length = response.data.length;

            // Check if the number of players is less than or equal to 3
        
              // Populate the batsmen array with id and name from playerlist

              // Display the selected team and category as a Swal message
              Swal.fire({
                icon: "success",
                title: "Great choice!",
                html: `
              Winner of the toss  <b>${selectedTeam.name}</b> elected to  <b>${selectedCategory.name}</b>`,
              }).then(() => {
                // Reset the selections after the Swal message is closed
                this.selectedCardId = null;
                this.selectedcategoryCardId = null;
                if (selectedCategory.name == "BOWL") {
                  this.startMatch(
                    nonSelectedTeam.name,
                    "BAT",
                    nonSelectedTeam.id,
                    selectedTeam.id,
                    selectedTeam.name
                  );
                } else {
                  this.startMatch(
                    selectedTeam.name,
                    selectedCategory.name,
                    selectedTeam.id,
                    nonSelectedTeam.id,
                    nonSelectedTeam.name
                  );
                }
              });
            
          },
          (error) => {
            const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
            this.$toast.show(errorMessage, {
            type: "error",
          });
          }
        );
      }
    },
    startMatch(team, category, id, nonSelectedTeam, nonSelectedTeamId) {
      const encodedId = btoa(this.MatchId + "tournamentMatch");
      const encodedtournamentId = btoa(this.tournamentId + "tournamentMatch");
      const encodedTeam = btoa(team + "tournamentMatch");
      const encodedTeamId = btoa(id + "tournamentMatch");
      const nonSelectedencodedTeam = btoa(nonSelectedTeam + "tournamentMatch");
      const nonSelectedencodedTeamId = btoa(
        nonSelectedTeamId + "tournamentMatch"
      );
      const encodedCategory = btoa(category + "tournamentMatch");

      this.$router.push({
        name: "match-scoring",
        params: {
          tournamentId: encodedtournamentId,
          MatchId: encodedId,
          team: encodedTeam,
          category: encodedCategory,
          id: encodedTeamId,
          nonSelectedId: nonSelectedencodedTeam,
          nonSelectedTeam: nonSelectedencodedTeamId,
        },
        // Replace "match-scoring" with the actual name of the next page's route
      });
    },
  },
};
</script>
<style scoped>
.card {
  box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
}
.selected-card {
  border: 2px solid #00bfff;
}
</style>
