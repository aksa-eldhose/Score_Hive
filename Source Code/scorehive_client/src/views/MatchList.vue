<template>
  <NavBar />
  <div class="container mt-4" style="min-height: 20vh; width: 65%">
    <div class="card mb-4 shadow">
      <div class="card-body">
        <div class="col-md-12">
          <div class="d-flex justify-content-between">
            <div class="col-md-6 mt-1">
              <h3 class="text-start">Matches</h3>
            </div>
            <div
              class="col-md-2"
              :style="{
                cursor: isEnded ? 'not-allowed' : 'pointer',
              }"
            >
              <cbutton
                class="btn btn-primary"
                color="primary"
                :disabled="isEnded"
                @click="scheduleMatch"
              >
                Schedule Match</cbutton
              >
            </div>
          </div>
        </div>
        <div class="row tab-content">
          <div class="col-md-12"></div>
        </div>
        <!--Table-->
        <div v-if="!isLoading">
          <div class="table-responsive">
            <table
              class="table table-hover text-center"
              style="border-collapse: collapse"
              aria-label=""
            >
              <!-- Table head -->
              <thead style="margin-bottom: 0">
                <tr>
                  <th id="" class="text-start ps-4">Macth Between</th>
                  <th id="" class="text-start">City</th>
                  <th id="" class="text-start">Ground</th>
                  <th id="" class="text-start">Date&Time</th>
                  <th id="" class="text-start">Actions</th>
                </tr>
              </thead>
              <!-- Table body -->
              <tbody class="tab-pane" id="my-teams" role="tabpanel">
                <tr v-if="isListEmpty()">
                  <td colspan="4">
                    <img
                      :src="listEmpty"
                      alt="Image"
                      style="margin-top: 10px"
                    />
                    <p>
                      There are no matches scheduled yet. schedule matches now.
                    </p>
                  </td>
                </tr>
                <tr v-for="match in matchlist" :key="match.id">
                  <td class="text-start ps-4">
                    {{ match.team1.name }} vs {{ match.team2.name }}
                  </td>
                  <td class="text-start">
                    {{ match.city.name }}
                  </td>
                  <td class="text-start">
                    {{ match.ground.name }}
                  </td>
                  <td class="text-start">
                    {{ match.date_time }}
                  </td>
                  <td>
                    <div class="d-flex justify-content-start">
                      <span
                        style="
                          cursor: pointer;
                          margin-right: 10px;
                          margin-left: 5px; /* Adjusted margin-right value */
                          border: none;
                          background-color: transparent;
                        "
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Start Match"
                        @click=" isEnded ? null :
                          matchTossRout(
                            match.id,
                            match.team1.name,
                            match.team2.name,
                            match.team1.id,
                            match.team2.id
                          )
                        "
                        :style="{
                          cursor: isEnded ? 'not-allowed' : 'pointer',
                          color: isEnded
                            ? 'rgb(172, 63, 63)'
                            : 'rgb(184, 38, 38)',
                        }"
                      >
                        <i
                          class="fa fa-play fa-lg"
                          :class="{ 'disabled-icon': isEnded }"
                          style="color: rgb(106, 99, 145)"
                        ></i>
                      </span>
                      <span
                        style="
                          cursor: pointer;
                          margin-right: 10px;
                          margin-left: 15px; /* Adjusted margin-right value */
                          border: none;
                          background-color: transparent;
                        "
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Edit"
                        @click="isEnded ? null : updateMatch"
                        :style="{
                          cursor: isEnded ? 'not-allowed' : 'pointer',
                          color: isEnded
                            ? 'rgb(172, 63, 63)'
                            : 'rgb(184, 38, 38)',
                        }"
                      >
                        <i
                          class="fa fa-pencil fa-md"
                          :class="{ 'disabled-icon': isEnded }"
                          style="color: rgb(41, 109, 55)"
                        ></i>
                      </span>
                      <span
                        style="
                          cursor: pointer;
                          margin-right: 10px;
                          margin-left: 15px; /* Adjusted margin-right value */
                          border: none;
                          background-color: transparent;
                        "
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Delete"
                        @click="isEnded ? null : deleteMatch(match.id)"
                        :style="{
                          cursor: isEnded ? 'not-allowed' : 'pointer',
                          color: isEnded
                            ? 'rgb(172, 63, 63)'
                            : 'rgb(184, 38, 38)',
                        }"
                      >
                        <i
                          :class="{ 'disabled-icon': isEnded }"
                          :disabled="isEnded"
                          class="fa fa-trash fa-md"
                          style="color: rgb(184, 38, 38)"
                        ></i>
                      </span>

                      <div class="dropdown">
                        <span
                          style="
                            cursor: pointer;
                            margin-right: 10px;
                            margin-left: 15px;
                          "
                          data-bs-toggle="tooltip"
                          data-bs-placement="top"
                          title="Settings"
                        >
                          <i class="fa fa-cog fa-md" style="color: #154ea3"></i>
                        </span>

                        <div
                          class="dropdown-content text-start"
                          v-show="active"
                        >
                          <a></a>
                        </div>
                      </div>
                    </div>
                  </td>

                  <td></td>
                </tr>
              </tbody>
            </table>
            <!--For pagination-->
            <div class="d-flex justify-content-center">
              <nav
                aria-label="Page navigation example"
                style="margin-right: 25px"
              >
                <cbutton
                  class="btn btn-primary"
                  color="primary"
                  disabled
                  style="margin-right: 10px"
                >
                  &laquo; Previous</cbutton
                >
                <cbutton class="btn btn-primary" color="primary" disabled>
                  Next &raquo;
                </cbutton>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import NavBar from "./NavBar.vue";
import errorCodes from "@/services/errorCodes.json";
import Swal from "sweetalert2";
import cbutton from "@/components/Button.vue";
import listEmpty from "@/assets/img/empty-list-team.jpg";
import { getTournamentById } from "@/services/tournamentService";
import {
  tournamentMatchList,
  removeTournamentMatch,
  tournamentMatchListPages
} from "@/services/matchService";
import { playerList } from "@/services/playerService";

export default {
  components: {
    cbutton,
    NavBar,
  },
  data() {
    return {
      matchlist: {},
      active: false,
      isEnded: false,
      listEmpty,
      playerlist2: [],
      playerlist1: [],
    };
  },
  mounted() {
    if (this.$route?.params?.TournamentId) {
      const secret = "tournamentMatch";
      try {
        this.tournamentId = atob(this.$route?.params?.TournamentId).replace(
          secret,
          ""
        );
      } catch (error) {
        this.$router.push("not-found");
      }
    }
    this.getTournamentDetails();
    this.tournamentMatch();
  },
  methods: {
    tournamentMatch() {
      tournamentMatchList(this.tournamentId).then(
        (response) => {
          this.matchlist = response.data.results;
          
        },
        (error) => {
          this.matchlist = { results: [] };
          const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
        }
      );
    },
    getTournamentDetails() {
      getTournamentById(this.tournamentId).then(
        (response) => {
          const currentDate = new Date().toISOString().split("T")[0];
          if (response.data.end_date < currentDate) {
            this.isEnded = true;
          }
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
    },
    scheduleMatch() {
      const encodedId = btoa(this.tournamentId + "tournamentSchdedule");
      this.$router.push({
        name: "schedule-match",
        params: { TournamentId: encodedId },
      });
    },
    updateMatch() {
      const encodedId = btoa(this.tournamentId + "tournamentUpdate");
      this.$router.push({
        name: "Update-match",
        params: { TournamentId: encodedId },
      });
    },

    deleteMatch(matchId) {
      Swal.fire({
        text: "Are you sure you want to delete this round?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
      }).then((result) => {
        if (result.isConfirmed) {
          removeTournamentMatch(Number(matchId)).then(
            () => {
              Swal.fire({
                icon: "success",
                text: "Deleted successfully",
              }).then(() => {});
              this.tournamentMatch();
            },
            (error) => {
              this.tournamentMatch();
              const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
            }
          );
        }
      });
    },

    matchByPage(data) {
      // method to call previous and next pages of the team list
      const pageRegex = /page=(\d+)/;
      const match = data.match(pageRegex);
      const page = match ? match[1] : null;
      if (page) {
        tournamentMatchListPages(this.tournamentId, page).then(
          (response) => {
            this.matchlist = response.data;
            window.scrollTo(0, 0);
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
      } else {
        this.tournamentMatch();
      }
    },

    isListEmpty() {
      //checks whether the team list is empty(no teams are added)
      return this.matchlist.length === 0;
    },
   async matchTossRout(id, team1, team2, id1, id2) {
      await playerList(id1).then(
        (response) => {
          this.playerlist1 = response.data;
          this.playerlist1Length = response.data.length;
          // Populate the batsmen array with id and name from playerlist
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
     await playerList(id2).then(
        (response) => {
          this.playerlist2 = response.data;
          this.playerlist2Length = response.data.length;
          // Populate the batsmen array with id and name from playerlist
        },
        (error) => { const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });}
      );
      if (this.playerlist2Length < 3 || this.playerlist1Length < 3) {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "teams should have atleast 3 players!",
        });
      }
      else
      { 
      const encodedId = btoa(id + "tournamentMatch");
      const encodedtournamentId = btoa(this.tournamentId + "tournamentMatch");
      const encodedTeam1 = btoa(team1 + "tournamentMatch");
      const encodedTeam2 = btoa(team2 + "tournamentMatch");
      const encodedteam1Id = btoa(id1 + "tournamentMatch");
      const encodedteam2Id = btoa(id2 + "tournamentMatch");
      this.$router.push({
        name: "match-toss",
        params: {
          MatchId: encodedId,
          tournamentId: encodedtournamentId,
          id1: encodedteam1Id,
          id2: encodedteam2Id,
          team1: encodedTeam1,
          team2: encodedTeam2,
        },
      });
    }
     
    },
  },
};
</script>
<style scoped>
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  /* display: list-item; */
}

.dropdown-content a:hover {
  background-color: #ddd;
}
.dropdown {
  /* position: relative; */
  display: block;
}
.dropdown-content {
  position: absolute;
  z-index: 1;
  top: -100%; /* Position the dropdown above the button */
  right: 0;
  display: none;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  padding: 12px 16px;
}

.dropdown:hover .dropdown-content {
  display: block;
  min-width: 60px;
}
.disabled-icon {
  opacity: 0.5;
}
.lightboxContainer {
  position: relative;
  display: inline-block;
}

.lightboxContainer:after {
  content: url("https://www.wonderplugin.com/download/playbutton.png");
  z-index: 999;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-left: -32px;
  margin-top: -32px;
}

.lightboxContainer img {
  width: 100px;
}
</style>
