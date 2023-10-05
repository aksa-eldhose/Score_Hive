<template>
  <NavBar />
  <div class="container mt-4">
    <div class="card mb-4 shadow">
      <div class="card-body">
        <div class="row align-items-center underline">
          <div class="col-md-6 mt-1">
            <h3 class="text-start">Teams</h3>
          </div>
          <div
            class="col-md-6"
            :style="{
              cursor: isEnded || isTblLoading ? 'not-allowed' : 'pointer',
            }"
          >
            <ButtonComponent
              color="primary"
              style="margin-left: 80%; width: 20%"
              @click="openModal"
              :disabled="isEnded || isTblLoading"
              id="addtournament"
            >
              <span
                v-if="isTblLoading"
                class="spinner-border spinner-border-sm me-2"
                role="status"
                aria-hidden="true"
              ></span>
              <span v-else>ADD TEAM</span>
            </ButtonComponent>
            <modal :show="modalOpen" @close="closeModal" />
          </div>
        </div>
        <div class="row">
          <div class="col-md-12"></div>
        </div>
        <!--Table-->
        <div>
          <div class="table-responsive">
            <table 
              class="table table-hover text-center"
              style="border-collapse: collapse" aria-label=""
            >
              <!-- Table head -->
              <thead style="margin-bottom: 0">
                <tr>
                  <th id=""
                    style="
                      width: 10%;
                      padding: 10px 20px 10px 50px;
                      text-align: left;
                    "
                  >
                    Id
                  </th>
                  <th id="" style="width: 10%; padding: 10px; text-align: left">
                    Team Name
                  </th>
                  <th id="" style="width: 10%; padding: 10px; text-align: left">
                    Members
                  </th>
                  <th id=""
                    style="
                      width: 5%;
                      padding: 20px;
                      text-align: left;
                      padding-bottom: 10px;
                    "
                  >
                    Action
                  </th>
                </tr>
              </thead>
              <!-- Table body -->
              <tbody>
                <tr v-if="isListEmpty() && !isTblLoading">
                  <td colspan="4">
                    <img
                      :src="listEmpty"
                      alt="Image"
                      style="margin-top: 10px"
                    />
                    <p>
                      There are no teams added into the tournament yet.Add teams
                      now.
                    </p>
                  </td>
                </tr>
                <tr
                  v-else-if="!isTblLoading"
                  v-for="team in teamlist"
                  :key="team.id"
                >
                  <td style="text-align: left; padding: 10px 20px 10px 50px">
                    {{ team.id }}
                  </td>
                  <td style="text-align: left">{{ team.name }}</td>
                  <td style="text-align: left">
                    <a @click="tournamentTeamPlayers(team.id)" class="link"
                      >Members</a
                    >
                  </td>
                  <td>
                    <div style="text-align: left; margin-left: 19%">
                      <span
                        @click="isEnded ? null : removeTeam(team.id)"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Remove team"
                        :style="{
                          cursor: isEnded ? 'not-allowed' : 'pointer',
                          color: isEnded
                            ? 'rgb(172, 63, 63)'
                            : 'rgb(184, 38, 38)',
                        }"
                      >
                        <i
                          class="fa fa-times-circle fa-lg"
                          :class="{ 'disabled-icon': isEnded }"
                        ></i>
                      </span>
                    </div>
                  </td>
                </tr>
                <tr v-else>
                  <td colspan="4" class="text-center">
                    <div
                      v-if="isTblLoading"
                      class="d-flex justify-content-center align-items-center"
                      style="height: 100px"
                    >
                      <div class="spinner-border" role="status">
                        <span class="visually-hidden">Loading...</span>
                      </div>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
  <Modal :show="modalOpen" @close="closeModal">
    <div class="modal-header">
      <h4 class="modal-title">Teams</h4>
      <button
        type="button"
        class="btn-close"
        data-mdb-dismiss="modal"
        @click="closeModal"
      ></button>
    </div>
    <div class="modal-body">
      <!-- Add your modal content here -->
      <div class="d-flex justify-content-end mb-2 px-1 pb-1">
        <input
          class="form-control w-50"
          type="text"
          v-model="search_term"
          placeholder="Search"
        />
      </div>
      <form v-if="!isModalLoading">
        <div class="form-group overflow-auto" style="max-height: 50vh">
          <div
            class="card mb-1 shadow"
            v-for="team in teamlistToAdd"
            :key="team.id"
          >
            <div
              class="card-body d-flex justify-content-between align-items-center"
            >
              <span
                v-b-tooltip.hover
                :title="team.name.length > 20 ? team.name : ''"
              >
                {{
                  team.name.length > 20
                    ? truncateText(team.name, 20)
                    : team.name
                }}
              </span>
              <ButtonComponent
                @click.prevent="addToTournament(team.id)"
                :disabled="isLoading"
                color="primary"
              >
                <span
                  v-if="isLoading && selectedTeamId === team.id"
                  class="spinner-border spinner-border-sm mx-2"
                  role="status"
                  aria-hidden="true"
                ></span>
                <span v-else>Add</span>
              </ButtonComponent>
            </div>
          </div>
          <div v-if="teamlistToAdd.length === 0" class="text-center">
            <img
              :src="emptyTeams"
              alt="Image"
              style="margin-top: 10px; width: 200px; height: 200px"
            /><br />
            <p style="font-size: small">{{ $t("No_teams_to_added") }}</p>
          </div>
        </div>
      </form>
      <div v-else class="d-flex justify-content-center align-items-center pb-3">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div class="modal-footer"></div>
    </div>
  </Modal>
</template>
<script>
import errorCodes from "@/services/errorCodes.json";
import Modal from "../components/ModalComponent.vue";
import NavBar from "./NavBar.vue";
import listEmpty from "@/assets/img/empty-list-team.jpg";
import "bootstrap-icons/font/bootstrap-icons.css";
import Swal from "sweetalert2";
import {
  tournamentTeamList,
  addTeamsToTournament,
  removeTournamentTeam,
  getTournamentById,
} from "@/services/tournamentService";
import ButtonComponent from "@/components/Button.vue";
import emptyTeams from "@/assets/img/logos/folder_empty.jpg";
import debounce from "lodash.debounce";
export default {
  components: {
    NavBar,
    Modal,
    ButtonComponent,
  },
  data() {
    return {
      teamlist: [],
      teamlistToAdd: [],
      listEmpty,
      modalOpen: false,
      tournamentId: "",
      isLoading: false,
      selectedTeamId: "",
      isEnded: false,
      isModalLoading: false,
      isTblLoading: false,
      isBtnDisabled: false,
      emptyTeams,
      search_term: "",
    };
  },
  watch: {
    search_term: {
      handler: debounce(function (search_term) {
        this.fetchTeams(this.tournamentId, 0, search_term);
      }, 500),
      immediate: false, // Set to true if you want to call fetchTeams immediately on component mount.
    },
  },
  mounted() {
    if (this.$route?.params?.TournamentId) {
      const secret = "tournamentTeams";
      try {
        this.tournamentId = atob(this.$route?.params?.TournamentId).replace(
          secret,
          ""
        );
      } catch (error) {
        this.$router.push("not-found");
      }
    }
    this.fetchTeams(this.tournamentId, 1, this.search_term);
    this.getTournaentDetails();
  },
  methods: {

    tournamentTeamPlayers(teamId) {
      const encodedId = btoa(teamId + "Team");
      this.$router.push({
        name: "player-list",
        params: { teamId: encodedId },
      });
    }, 
    truncateText(text, limit) {
      if (text.length > limit) {
        return text.slice(0, limit) + "...";
      }
      return text;
    },
    isListEmpty() {
      //checks whether the team list is empty(no teams are added)
      return this.teamlist.length === 0;
    },
    openModal() {
      this.fetchTeams(this.tournamentId, 0, this.search_term);
      this.modalOpen = true;
    },
    closeModal() {
      this.fetchTeams(this.tournamentId, 1, this.search_term);
      this.modalOpen = false;
    },
    fetchTeams(tournamentId, flag, search_term) {
      this.isModalLoading = true;
      this.isTblLoading = true;
      tournamentTeamList(tournamentId, flag, search_term).then(
        (response) => {
          if (flag === 1) {
            this.teamlist = response.data;
            this.isTblLoading = false;
          } else if (flag === 0) {
            this.teamlistToAdd = response.data;
            this.isModalLoading = false;
          }
        },
        () => {
          this.isModalLoading = false;
          this.teamlist = [];
          this.isTblLoading = false;
        }
      );
    },
    //Add the teams to tournament
    addToTournament(teamId) {
      this.selectedTeamId = teamId;
      let param = {
        tournament_id: +this.tournamentId,
        team_id: +teamId,
      };
      this.isLoading = true;
      addTeamsToTournament(param).then(
        () => {
          this.$toast.show("Team is added to the tournament successfully", {
            type: "success",
          });
          this.fetchTeams(this.tournamentId, 0, this.search_term);
          setTimeout(() => {
            this.isLoading = false; // Set isLoading to false after a delay
          }, 1000);
        },
        (error) => {
          const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
          setTimeout(() => {
            this.isLoading = false; // Set isLoading to false after a delay
          }, 1000);
        }
      );
    },
    removeTeam(teamId) {
      this.isBtnDisabled = true;
      let param = {
        tournament_id: +this.tournamentId,
        team_id: +teamId,
      };
      Swal.fire({
        text: "Are you sure you want to remove this team from the tournament?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Remove",
        cancelButtonText: "Cancel",
      }).then((result) => {
        if (result.isConfirmed) {
          this.isTblLoading = true;
          removeTournamentTeam(param).then(
            () => {
              this.$toast.show(
                "Team removed from the tournament successfully",
                {
                  type: "success",
                }
              );
              this.fetchTeams(this.tournamentId, 1, this.search_term);
              this.isBtnDisabled = false;
            },
            (error) => {
              this.isBtnDisabled = false;
              const errorMessage =
                errorCodes[error.response.data.error_code] ||
                "Oops.. Some unknown error occurred..!";
              this.$toast.show(errorMessage, {
                type: "error",
              });
            }
          );
        } else {
          this.isBtnDisabled = false;
        }
      });
    },
    getTournaentDetails() {
      getTournamentById(this.tournamentId).then(
        (response) => {
          const currentDate = new Date().toISOString().split("T")[0];
          if (response.data.end_date < currentDate) {
            this.isEnded = true;
          }
        },
        () => {
        this.$toast.error("Oops!Some unknown error occured..");
        }
      );
    },
  },
};
</script>
<style scoped>
.underline {
  border-bottom: 1px solid #f2f2f2;
}
.remove {
  border: none;
  background-color: transparent;
  margin-left: 10px;
}
.icon-large {
  font-size: 1.4rem;
  font-weight: 1000;
  color: rgb(194, 68, 68);
}
.icon-large:hover {
  color: rgb(240, 49, 49);
}
.btn-small {
  padding: 0.125rem 0.25rem;
  font-size: 0.75rem;
}
.disabled-icon {
  opacity: 0.5;
}
</style>
