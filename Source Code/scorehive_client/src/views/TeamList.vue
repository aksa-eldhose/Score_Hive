<template>
  <NavBar />
  <div class="container mt-4">
    <div class="card mb-4 shadow">
      <div class="card-body">
        <div class="col-md-12">
          <div class="d-flex align-items-center mt-0 mb-0">
            <ul class="nav nav-tabs mt-0" role="tablist">
              <li class="nav-item">
                <a
                  class="nav-link"
                  role="tab"
                  :class="{ active: selectedTab === 'my-teams' }"
                  @click="selectedTab = 'my-teams'"
                  style="font-size: 18px"
                  :style="{ color: selectedTab === 'my-teams' ? 'blue' : '#4b4949' }"
                  >My Teams</a
                >
              </li>
              <li class="nav-item">
                <a
                  class="nav-link"
                  role="tab"
                  :class="{ active: selectedTab === 'joined-teams' }"
                  @click="selectedTab = 'joined-teams'"
                  style="font-size: 18px"
                  :style="{ color: selectedTab === 'joined-teams' ? 'blue' : '#4b4949' }"
                  >Joined Teams</a
                >
              </li>
            </ul>
            <ButtonComponent
              color="primary"
              style="margin-left: 63%"
              @click="createTeam"
            >
              CREATE TEAM
            </ButtonComponent>
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
                  <th  id="" style="width: 10%; padding: 10px; text-align: left">
                    Members
                  </th>
                  <th id="" style="width: 5%; padding: 20px; text-align: left">
                    Actions
                  </th>
                </tr>
              </thead>
              <!-- Table body -->
              <tbody
                v-show="selectedTab === 'my-teams'"
                class="tab-pane"
                id="my-teams"
                role="tabpanel"
              >
                <tr v-if="isListEmpty()">
                  <td colspan="4">
                    <img
                      :src="listEmpty"
                      alt="Image"
                      style="margin-top: 10px"
                    />
                    <p>There are no teams added yet. Add teams now.</p>
                  </td>
                </tr>
                <tr v-else v-for="team in teamlist.results" :key="team.id">
                  <td style="text-align: left; padding: 10px 20px 10px 50px">
                    {{ team.id }}
                  </td>
                  <td style="text-align: left; padding: 11px">
                    {{ team.name }}
                  </td>
                  <td style="text-align: left; padding: 11px">
                    <a
                      href="#"
                      class="text-primary d-inline text-decoration-underline"
                      @click="viewTournamentDetail(team.id)"
                    >
                      Members
                    </a>
                  </td>
                  <td>
                    <div style="text-align: left; margin-left: 25px">
                      <span
                        @click="editTeam(team.id)"
                        style="cursor: pointer; margin-right: 10px"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Edit"
                      >
                        <i
                          class="fa fa-pencil fa-md"
                          style="color: rgb(41, 109, 55)"
                        ></i>
                      </span>
                      <span
                        @click="deleteTeam(team.id)"
                        style="cursor: pointer; margin-left: 10px"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Delete"
                      >
                        <i
                          class="fa fa-trash fa-md"
                          style="color: rgb(184, 38, 38)"
                        ></i>
                      </span>
                    </div>
                  </td>
                </tr>
              </tbody>
              <tbody
                v-show="selectedTab === 'joined-teams'"
                class="tab-pane"
                id="my-teams"
                role="tabpanel"
              >
                <tr v-if="isJoinEmpty()">
                  <td colspan="4">
                    <img
                      :src="listEmpty"
                      alt="Image"
                      style="margin-top: 10px"
                    />
                    <p>You have not joined to any team.</p>
                  </td>
                </tr>
                <tr
                  v-else
                  v-for="team in joinedTeamList.results"
                  :key="team.id"
                >
                  <td style="text-align: left; padding: 10px 20px 10px 50px">
                    {{ team.id }}
                  </td>
                  <td style="text-align: left; padding: 11px">
                    {{ team.name }}
                  </td>
                  <td style="text-align: left; padding: 11px">
                    <a
                      href="#"
                      class="text-primary d-inline text-decoration-underline"
                      @click="viewplayerDetail(team.id)"
                    >
                      Members
                    </a>
                  </td>
                  <td>
                    <div style="text-align: left; margin-left: 19%">
                      <span
                        @click="exitTeam(team.id)"
                        style="cursor: pointer"
                        data-bs-toggle="tooltip"
                        data-bs-placement="top"
                        title="Exit Team"
                      >
                        <i
                        class="bi bi-box-arrow-right"
                        style="color: rgb(190, 11, 11); font-size: 18px;"
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
              v-if="!isListEmpty()"
              v-show="selectedTab === 'my-teams'"
            >
              <ButtonComponent
                class="btn btn-primary"
                color="primary"
                @click="teamByPage(teamlist.previous)"
                :disabled="teamlist.previous == null"
                style="margin-right: 10px"
              >
                &laquo; Previous</ButtonComponent
              >
              <ButtonComponent
                class="btn btn-primary"
                color="primary"
                @click="teamByPage(teamlist.next)"
                :disabled="teamlist.next == null"
              >
                Next &raquo;
              </ButtonComponent>
            </nav>
          </div>
          </div>
        </div>
        <div v-else></div>
      </div>
    </div>
  </div>
</template>
<script>
import Swal from "sweetalert2";
import NavBar from "./NavBar.vue";
import "bootstrap-icons/font/bootstrap-icons.css";
import { teamList, teamListPages, teamDelete } from "@/services/authService";
import { getJoinedTeams,exitFromTeam } from "@/services/teamService";
import listEmpty from "@/assets/img/empty-list-team.jpg";
import ButtonComponent from "@/components/Button.vue";
export default {
  name: "team-list",
  components: {
    NavBar,
    ButtonComponent,
  },
  mounted() {
    /**Fetching team list */
    this.getTeamList();
    this.getJoinedTeamsList();

  },
  data() {
    return {
      teamlist: [],
      reachLimit: false,
      listEmpty,
      isLoading: true,
      selectedTab: "my-teams",
      joinedTeamList: [],
    };
  },
  methods: {
    getTeamList() {
      this.isLoading = true;
      teamList()
        .then(
          (response) => {
            this.teamlist = response.data;
            window.scrollTo(0, 0);
          },
          (error) => {  
            if (error.response.data.error_code == 4012) {
                this.teamlist=[]
              }
          }
        )
        .finally(() => {
          this.isLoading = false; // Hide loading message
        });
    },
    getJoinedTeamsList() {
      this.isLoading = true;
      getJoinedTeams()
        .then(
          (response) => {
            this.joinedTeamList = response.data;
            window.scrollTo(0, 0);
          },
          (error) => {
            if (error.response.data.error_code == 4012) {
                this.joinedTeamList=[]
              }
          }
        )
        .finally(() => {
          this.isLoading = false; // Hide loading message
        });
    },
    addTeam() {
      //method to navigate to the add team page
      this.$router.push({
        name: "CreateTeam",
      });
    },
    editTeam(teamid) {
      // method to navigate to the edit team page
      this.$router.push({
        name: "UpdateTeam",
        query: { teamId: teamid },
      });
    },
    exitTeam(teamid) {
      Swal.fire({
        text: "Are you sure you want to exit from this team?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Exit",
        cancelButtonText: "Cancel",
      }).then((result) => {
        if (result.isConfirmed) {
          exitFromTeam(teamid).then(
            () => {
              Swal.fire({
                icon: "success",
                text: "You are exited from the team successfully!!",
              }).then(() => {
                this. selectedTab = "joined-teams"
                this. getJoinedTeamsList();

              });
            },
            () => {
              this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });
            }
          );
        }
      });
      
    },
    isListEmpty() {
      //checks whether the team list is empty(no teams are added)
      return this.teamlist.length === 0;
    },
    isJoinEmpty() {
      //checks whether the team list is empty(no teams are added)
      return this.joinedTeamList.length === 0;
    },
    teamByPage(data) {
      // method to call previous and next pages of the team list
      const pageRegex = /page=(\d+)/;
      const match = data.match(pageRegex);
      const page = match ? match[1] : null;
      if (page) {
        teamListPages(page).then(
          (response) => {
            this.teamlist = response.data;
            window.scrollTo(0, 0);
          },
          () => {  this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });}
        );
      } else {
        this.getTeamList();
      }
    },
    viewTeamMembers(teamId) {
      this.$router.push({ name: "player-list", params: { teamId } });
    },
    viewTournamentDetail(Id) {
      const encodedId = btoa(Id + "Team");
      this.$router.push({
        name: "player-list",
        params: { teamId: encodedId },
      });
    }, 
    viewplayerDetail(Id) {
      const encodedId = btoa(Id + "Team");
      this.$router.push({
        name: "Joined-player-list",
        params: { teamId: encodedId },
      });
    },
    deleteTeam(teamId) {
      Swal.fire({
        text: "Are you sure you want to delete this record?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Delete",
        cancelButtonText: "Cancel",
      }).then((result) => {
        if (result.isConfirmed) {
          teamDelete(teamId).then(
            () => {
              Swal.fire({
                icon: "success",
                text: "Deleted successfully",
              }).then(() => {
                window.location.reload();
              });
            },
            () => {  this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });}
          );
        }
      });
    },
    createTeam() {
      this.$router.push({
        name: "CreateTeam",
      });
    },
  },
};
</script>
<style scoped>
.nav-link.active {
  color: hsl(218, 41%, 15%);
}
@media (max-width: 768px) {
  .AddTeam {
    margin-left: 0;
  }
}
.paginationItem {
  margin-left: 40%;
}
.page-item {
  text-decoration: none;
  display: inline-block;
  padding: 5px 10px;
  font-size: 15px;
  background-color: hsl(218, 41%, 15%);
  color: rgb(201, 201, 209);
}
.page-item[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
.underline {
  border-bottom: 1px solid #f2f2f2;
}
</style>
