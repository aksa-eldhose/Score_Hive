<template>
  <NavBar />
  <div class="container mt-4" style="min-height: 20vh; width: 65%">
    <div class="card mb-4 shadow">
      <div class="card-body">
        <div class="col-md-12">
          <div class="d-flex justify-content-between">
            <div class="col-md-6 mt-1">
              <h3 class="text-start">Rounds</h3>
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
                style="margin-left: 40%"
                @click.prevent="addRound()"
                :disabled="isEnded"
              >
                Add Round</cbutton
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
                  <th
                    id=""
                    style="
                      width: 10%;
                      padding: 10px 20px 10px 50px;
                      text-align: left;
                    "
                  >
                    Id
                  </th>
                  <th
                    id=""
                    style="
                      width: 10%;
                      padding: 10px 20px 10px 50px;
                      text-align: left;
                    "
                  >
                    Round
                  </th>

                  <th id="" style="width: 5%; padding: 20px; text-align: left">
                    Actions
                  </th>
                </tr>
              </thead>
              <!-- Table body -->
              <tbody class="tab-pane" id="my-teams" role="tabpanel">
                <tr v-if="this.roundlist.results?.length == 0">
                  <td colspan="4">
                    <img
                      :src="listEmpty"
                      alt="Image"
                      style="margin-top: 10px"
                    />
                    <p>There are no rounds added yet. Add rounds now.</p>
                  </td>
                </tr>
                <tr
                  v-else
                  v-for="round in roundlist.results"
                  :key="round.round_id"
                >
                  <td style="text-align: left; padding: 10px 20px 10px 50px">
                    {{ round.round_id }}
                  </td>
                  <td style="text-align: left; padding: 10px 20px 10px 50px">
                    {{ round.name }}
                  </td>
                  <td>
                    <div style="text-align: left; margin-left: 25px">
                      <span
                        @click="isEnded ? null : deleteRound(round.round_id)"
                        style="cursor: pointer; margin-left: 10px"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Delete"
                        :style="{
                          cursor: isEnded ? 'not-allowed' : 'pointer',
                        }"
                      >
                        <i
                          class="fa fa-trash fa-md"
                          :class="{ 'disabled-icon': isEnded }"
                          style="color: rgb(184, 38, 38)"
                        ></i>
                      </span>
                    </div>
                  </td>
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
                  @click="roundByPage(roundlist.previous)"
                  :disabled="roundlist.previous == null"
                  style="margin-right: 10px"
                >
                  &laquo; Previous</cbutton
                >
                <cbutton
                  class="btn btn-primary"
                  color="primary"
                  @click="roundByPage(roundlist.next)"
                  :disabled="roundlist.next == null"
                >
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
import Swal from "sweetalert2";
import cbutton from "@/components/Button.vue";
import listEmpty from "@/assets/img/empty-list-team.jpg";
import { getTournamentById } from "@/services/tournamentService";
import {
  tournamentRoundList,
  removeTournamentRound,
  tournamentRoundListPages,
} from "@/services/roundService";
import errorCodes from "@/services/errorCodes.json";

export default {
  components: {
    cbutton,
    NavBar,
  },
  data() {
    return {
      roundlist: {},
      listEmpty,
      isEnded: false,
      round_id: 0,
    };
  },
  mounted() {
    if (this.$route?.params?.TournamentId) {
      const secret = "tournamentRounds";
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
    this.tournamentRounds();
  },
  methods: {
    getTournamentDetails() {
      getTournamentById(this.tournamentId).then(
        (response) => {
          const currentDate = new Date().toISOString().split("T")[0];
          if (response.data.end_date < currentDate) {
            this.isEnded = true;
          }
        },
        (error) => {
          {
            const errorMessage =
              errorCodes[error.response.data.error_code] ||
              "Oops.. Some unknown error occurred..!";
            this.$toast.show(errorMessage, {
              type: "error",
            });
          }
        }
      );
    },
    deleteRound(round_id) {
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
          removeTournamentRound({
            tournament_id: Number(this.tournamentId),
            round_id: round_id,
          }).then(
            () => {
              Swal.fire({
                icon: "success",
                text: "Deleted successfully",
              });
              this.tournamentRounds();
            },
            (error) => {
              this.tournamentRounds();
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
    roundByPage(data) {
      // method to call previous and next pages of the team list
      const pageRegex = /page=(\d+)/;
      const match = data.match(pageRegex);
      const page = match ? match[1] : null;
      if (page) {
        tournamentRoundListPages(this.tournamentId, page).then(
          (response) => {
            this.roundlist = response.data;
            window.scrollTo(0, 0);
          },
          (error) => {
            {
              const errorMessage =
                errorCodes[error.response.data.error_code] ||
                "Oops.. Some unknown error occurred..!";
              this.$toast.show(errorMessage, {
                type: "error",
              });
            }
          }
        );
      } else {
        this.tournamentRounds();
      }
    },
    tournamentRounds() {
      tournamentRoundList(this.tournamentId).then(
        (response) => {
          this.roundlist = response.data;
        },
        (error) => {
          this.roundlist = { results: [] };
          const errorMessage =
              errorCodes[error.response.data.error_code] ||
              "Oops.. Some unknown error occurred..!";
            this.$toast.show(errorMessage, {
              type: "error",
            });
        }
      );
    },
    isListEmpty() {
      //checks whether the team list is empty(no teams are added)
      return this.roundlist.length === 0;
    },
    addRound() {
      this.$router.push({
        name: "add-rounds",
      });
    },
  },
};
</script>
<style scoped>
.disabled-icon {
  opacity: 0.5;
}
</style>
