<template>
  <NavBar />
  <div
    class="container py-5 h-100"
    v-if="this.list.results?.length === 0 && !apiCall"
  >
    <div class="row d-flex align-items-center justify-content-center h-100">
      <div class="col-md-8 col-lg-7 col-xl-6">
        <img
          :src="emptytournament"
          style="object-fit: scale-down; object-position: left"
          alt=""
        />
      </div>
      <div class="col-md-7 col-lg-5 col-xl-5 offset-xl-1">
        <h2><b>Hey there...!</b></h2>
        <p>
          Seems like you haven't created any tournament on ScoreHive. Go ahead
          and add a new tournament.
        </p>
        <cbutton
          class="btn btn-primary"
          color="primary"
          style="width: 160px; height: 45px; margin-left: 1%"
          @click="addtournament()"
        >
          ADD TOURNAMENT
        </cbutton>
      </div>
    </div>
  </div>
  <div class="container mt-4" v-if="this.list.results?.length !== 0">
    <div class="card mb-4 shadow">
      <div class="card-body">
        <div class="d-flex justify-content-between">
          <div class="col-md-6 mt-1">
            <h3 class="text-start">Tournaments</h3>
          </div>
          <div class="col-md-2">
            <cbutton
              class="btn btn-primary"
              color="primary"
              @click="addtournament()"
            >
              ADD TOURNAMENT
            </cbutton>
          </div>
        </div>
        <div class="table-responsive">
          <custom-table
            :columns="tableColums"
            :rows="list.results"
            class="table table-hover text-center"
            style="border-collapse: collapse"
          >
            <template v-slot:custom-columns>
              <th id="" class="text-start ps-4">Tournament Name</th>
              <th id="" class="text-start">Start Date</th>
              <th id="" class="text-start">End Date</th>
              <th id="" class="text-start">Actions</th>
              <th id="" class="text-start">Status</th>
            </template>
            <template v-slot:custom-rows="{ row }">
              <td class="text-start ps-4" :title="row.name">
                {{
                  showFullText
                    ? row.name
                    : row.name.slice(0, 20) +
                      (row.name.length > 20 ? "..." : "")
                }}
                <span v-if="!showFullText && row.name.length > 15"></span>
              </td>
              <td class="text-start">{{ row.start_date }}</td>
              <td class="text-start">{{ row.end_date }}</td>

              <td>
                <div class="d-flex justify-content-start">
                  <button
                    style="
                      cursor: pointer;

                      border: none;
                      background-color: transparent;
                    "
                    :style="{
                      cursor: isTournamentEnded(row.end_date)
                        ? 'not-allowed'
                        : 'pointer',
                    }"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    title="Edit"
                    :disabled="isTournamentEnded(row.end_date)"
                    @click="edittournament(row.id)"
                  >
                    <i
                      class="fa fa-pencil fa-md"
                      style="color: rgb(41, 109, 55)"
                      :style="{
                        color: isTournamentEnded(row.end_date)
                          ? 'rgba(41, 109, 55, 0.5)'
                          : 'rgb(41, 109, 55)',
                      }"
                    ></i>
                  </button>
                  <button
                    style="
                      cursor: pointer;

                      border: none;
                      background-color: transparent;
                    "
                    :style="{
                      cursor: isTournamentEnded(row.end_date)
                        ? 'not-allowed'
                        : 'pointer',
                    }"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top"
                    :disabled="isTournamentEnded(row.end_date)"
                    title="Delete"
                    @click="openModal(row.id)"
                  >
                    <i
                      class="fa fa-trash fa-md"
                      style="color: rgb(184, 38, 38)"
                      :style="{
                        color: isTournamentEnded(row.end_date)
                          ? 'rgba(184, 38, 38, 0.5)'
                          : 'rgb(184, 38, 38)',
                      }"
                    ></i>
                  </button>

                  <div class="dropdown">
                    <span
                      style="cursor: pointer; margin-left: 10px"
                      data-bs-toggle="tooltip"
                      data-bs-placement="top"
                      title="settings"
                      @click="toggleDropdown"
                      :disabled="isTournamentEnded(row.end_date)"
                    >
                      <i class="fa fa-cog fa-md" style="color: #154ea3"></i>
                    </span>

                    <div
                      class="dropdown-content text-start"
                      v-show="active"
                      @mouseleave="hideDropdown"
                    >
                      <a @click="tournamentTeams(row.id)">Teams</a>
                      <a @click="tournamentGroups(row.id)">Groups</a>
                      <a @click="tournamentRounds(row.id)">Rounds</a>
                      <a @click="tournamentMatch(row.id)">Matches</a>
                    </div>
                  </div>
                </div>
              </td>
              <td class="text-start">
                <span
                  v-if="isTournamentOngoing(row.start_date, row.end_date)"
                  class="badge rounded-pill bg-success"
                >
                  Ongoing
                </span>
                <span
                  v-else-if="isTournamentUpcoming(row.end_date)"
                  class="badge rounded-pill bg-warning"
                >
                  Upcoming
                </span>
                <span v-else class="badge rounded-pill bg-primary">
                  Completed
                </span>
              </td>
            </template>
          </custom-table>
          <div class="d-flex justify-content-center">
            <nav
              aria-label="Page navigation example"
              v-if="this.list.length != 0"
            >
              <Button
                class="btn btn-primary"
                color="primary"
                @click="tournamentByPage(list.previous)"
                :disabled="list.previous == null"
                style="margin-right: 10px"
              >
                &laquo; Previous</Button
              >
              <Button
                class="btn btn-primary"
                color="primary"
                @click="tournamentByPage(list.next)"
                :disabled="list.next == null"
              >
                Next &raquo;
              </Button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
  <modal :show="modalOpen" @close="closeModal">
    <div class="modal-header">
      <h4 class="modal-title">Delete tournament?</h4>
      <Button
        type="button"
        class="btn-close btn-close-black"
        data-mdb-dismiss="modal"
        @click="closeModal"
      ></Button>
    </div>
    <div class="modal-body">
      <!-- Add your modal content here -->
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Select reason</label>
          <div class="custom-control custom-radio custom-control-inline">
            <input
              type="radio"
              id="customRadioInline1"
              value="Created for testing"
              name="customRadioInline1"
              class="custom-control-input"
              v-model="reason"
            />&nbsp;
            <label class="custom-control-label" for="customRadioInline1"
              >Created for testing</label
            >
          </div>
          <div class="custom-control custom-radio custom-control-inline">
            <input
              type="radio"
              id="customRadioInline2"
              value="Others"
              name="customRadioInline1"
              class="custom-control-input"
              v-model="reason"
            />&nbsp;
            <label class="custom-control-label" for="customRadioInline2"
              >Others</label
            >
          </div>
        </div>
        <div class="row">
          <div class="col-md-12">
            <div class="form-group">
              <label>Description</label>
              <textarea
                id="comments"
                class="form-control"
                name="comment"
                placeholder="Enter your comment here..."
                :disabled="reason !== 'Others'"
                v-model="description"
              ></textarea>
              <div
                v-for="(error, index) in v$.description.$errors"
                :key="index"
                class="text-danger"
              >
                <span v-if="error.$params.type == 'maxLength'"
                  ><small>Tournament description is too long..!</small></span
                >
                <span v-if="error.$params.type == 'minLength'"
                  ><small>Description is too short..!</small></span
                >
              </div>

              <div
                v-for="error of v$.description.$errors"
                :key="error"
                class="text-danger"
              >
                <span v-if="error.$params.type == 'maxLength'"
                  ><small>Tournament description is too long..!</small></span
                >
                <span v-if="error.$params.type == 'minLength'"
                  ><small>Description is too short..!</small></span
                >
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <cbutton
            type="button"
            class="btn btn-danger"
            @click="removeTournaments()"
            :disabled="reason === ''"
          >
            DELETE
          </cbutton>
          <cbutton
            variant="outline"
            class="btn btn-outline-danger"
            color="primary"
            data-mdb-dismiss="modal"
            @click="closeModal"
          >
            CANCEL
          </cbutton>
        </div>
      </form>
    </div>
  </modal>

</template>
<script>
import Modal from "../components/ModalComponent.vue";
import CustomTable from "../components/TableComponent.vue";
import cbutton from "@/components/Button.vue";
import emptytournament from "@/assets/img/emptylist-tournament.jpg";
import Swal from "sweetalert2";
import errorCodes from "@/services/errorCodes.json";
import NavBar from "./NavBar.vue";
import "bootstrap-icons/font/bootstrap-icons.css";
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength, minLength } from "@vuelidate/validators";
import {
  tournamentList,
  tournamentListPages,
  removeTournament,
} from "@/services/tournamentService";
export default {
  name: "tournament-list",
  components: {
    NavBar,
    Modal,
    CustomTable,
    cbutton,
  },
  setup() {
    return { v$: useVuelidate() };
  },
  data() {
    return {
      list: {},
      currentPage: 1,
      perPage: 2,
      modalOpen: false,
      active: false,
      emptytournament,
      reason: "",
      description: "",
      isActive: true,
      showFullText: false,
      deleteId: 0,
      apiCall: false,
      selectedOption: null,
      options: [
        { value: "option1", label: "Option 1" },
        { value: "option2", label: "Option 2" },
        { value: "option3", label: "Option 3" },
      ],
    };
  },
  mounted() {
    /**Fetching tournament list */
    this.tournamentList();
  },
  validations() {
    return {
      reason: {
        required,
      },
      description: {
        maxLength: maxLength(255),
        minLength: minLength(1),
      },
    };
  },
  methods: {
    async removeTournaments() {
      const isValid = await this.v$.$validate();
      if (isValid) {
        removeTournament({
          tournament_id: this.deleteId,
          deleted_reason: this.$data.reason,
          description: this.$data.description,
        }).then(
          () => {
            this.closeModal();
            Swal.fire({
              icon: "success",
              text: "Deleted successfully",
            });
            this.tournamentList();
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
    tournamentList() {
      this.apiCall = true;
      tournamentList().then(
        (response) => {
          this.list = response.data;
          this.apiCall = false;
        },
        (error) => {
          this.list = { results: [] };
          this.apiCall = false;
          if (error.response.data.error_code == 5016) {
            this.list = { results: [] };
          }
        }
      );
    },
    tournamentGroups(id) {
      const encodedId = btoa(id + "tournamentGroups");
      this.$router.push({
        name: "group",
        params: { TournamentId: encodedId },
      });
    },
    tournamentRounds(id) {
      const encodedId = btoa(id + "tournamentRounds");
      this.$router.push({
        name: "list-rounds",
        params: { TournamentId: encodedId },
      });
    },
    tournamentMatch(id) {
      const encodedId = btoa(id + "tournamentMatch");
      this.$router.push({
        name: "match-list",
        params: { TournamentId: encodedId },
      });
    },
    isTournamentEnded(endDate) {
      const current_date = new Date().toISOString().split("T")[0];
      if (endDate < current_date) {
        return true;
      }
    },
    isTournamentOngoing(startDate, endDate) {
      const current_date = new Date().toISOString().split("T")[0];
      if (startDate <= current_date && endDate >= current_date) {
        return true;
      }
    },
    isTournamentUpcoming(startDate) {
      const current_date = new Date().toISOString().split("T")[0];
      if (startDate > current_date) {
        return true;
      }
    },
    addtournament() {
      this.$router.push({
        name: "add-tournament",
      });
    },

    tournamentByPage(data) {
      // method to call previous and next pages of the team list
      const pageRegex = /page=(\d+)/;
      const match = data.match(pageRegex);
      const page = match ? match[1] : null;
      if (page) {
        tournamentListPages(page).then(
          (response) => {
            this.list = response.data;
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
        this.tournamentList();
      }
    },
    toggleDropdown() {
      this.active = !this.active;
    },
    hideDropdown() {
      this.active = false;
    },
    openModal(id) {
      this.deleteId = id;
      this.modalOpen = true;
    },
    closeModal() {
      this.modalOpen = false;
      this.description = "";
      this.reason = "";
    },
    edittournament(tournamentId) {
      const secret = "tournament";
      const encodedId = btoa(tournamentId + secret);
      this.$router.push({
        name: "update-tournament",
        query: { tournamentId: encodedId },
      });
    },

    routes() {
      this.$router.push({
        name: "tournament-list",
      });
    },
    tournamentTeams(tournamentId) {
      const secret = "tournamentTeams";
      const encodedTournamentId = btoa(tournamentId + secret);
      this.$router.push({
        name: "tournament-teams",
        params: { TournamentId: encodedTournamentId },
      });
    },
  },
};
</script>
<style scoped>
.tooltip {
  border-radius: 50px;
}
.icons {
  font-size: 10px;
}
.iconbutton {
  color: #fff;
  background-color: #6c757d;
  border-color: #6c757d;
  display: inline-block;
  font-weight: 400;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  user-select: none;
  border: 1px solid transparent;
  padding: 0.1rem 0.5rem;
  font-size: 0.875rem;
  line-height: 1.5;
  border-radius: 0.25rem;
  transition: color 0.15s ease-in-out;
  /* Add margin-right to create space between buttons */
}
textarea.form-control {
  height: 160px;
  padding-top: 15px;
  resize: none;
}
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
  display: inline-block;
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

label {
  margin-bottom: 10px;
}
</style>
