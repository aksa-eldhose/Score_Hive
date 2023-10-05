<template>
  <div class="min-vh-100">
    <NavBar />
    <div>
      <div class="d-flex justify-content-center">
        <div
          class="card shadow-lg mx-lg-5 my-lg-5 bg-white p-4 h-100"
          style="min-height: 50vh; width: 70%"
        >
          <div
            class="d-flex justify-content-between align-items-center"
            :style="{
              cursor: isEnded ? 'not-allowed' : 'pointer',
            }"
          >
            <h4 class="text-dark">Groups</h4>
            <ButtonComponent
              :disabled="isEnded"
              color="primary"
              class="h-25"
              @click.prevent="addGroup()"
              >Add group</ButtonComponent
            >
          </div>
          <hr />
          <div
            v-if="emptyList()"
            class="text-center justify-content-center align-items-center"
          >
            <img :src="listEmpty" alt="Image" style="margin-top: 10px" /><br />
            <p style="font-size: medium">
              {{ $t("No_groups_are_added") }}
            </p>
          </div>
          <table
            v-if="!emptyList()"
            class="table table-hover text-center"
            style="border-collapse: collapse"
            aria-label=""
          >
            <thead style="margin-bottom: 0">
              <tr>
                <th
                  id=""
                  style="
                    width: 40%;
                    padding: 10px 10px 10px 90px;
                    text-align: left;
                  "
                >
                  No.
                </th>
                <th
                  id=""
                  style="
                    width: 40%;
                    padding: 10px 10px 10px 5px;
                    text-align: left;
                  "
                >
                  Group Name
                </th>
                <th
                  id=""
                  style="
                    width: 30%;
                    padding: 10px 10px 10px 8px;
                    text-align: left;
                  "
                >
                  Actions
                </th>
                <th id=""></th>
              </tr>
            </thead>

            <!-- Table body -->
            <tbody>
              <template v-for="(group, index) in grouplist" :key="index">
                <tr>
                  <td
                    style="
                      text-align: left;
                      width: 10%;
                      padding: 10px 10px 10px 90px;
                    "
                  >
                    {{ index + 1 }}
                  </td>
                  <td
                    style="
                      text-align: left;
                      width: 10%;
                      padding: 10px 10px 10px 5px;
                    "
                    :title="group.name"
                  >
                    {{
                      showFullText
                        ? group.name
                        : group.name.slice(0, 20) +
                          (group.name.length > 20 ? "..." : "")
                    }}
                  </td>
                  <td style="text-align: left">
                    <span
  @click="isEnded ? null : editGroup(group.id)"
  style="cursor: pointer; margin-right: 10px"
  data-bs-toggle="tooltip"
  data-bs-placement="top"
  title="Edit"
  :style="{ cursor: isEnded ? 'not-allowed' : 'pointer' }"
>
  <i
    class="fa fa-pencil fa-md"
    :class="{ 'disabled-icon': isEnded }"
    style="color: rgb(41, 109, 55)"
  ></i>
</span>

<span
  @click="isEnded ? null : deleteGroup(group.id)"
  style="cursor: pointer; margin-left: 10px"
  data-bs-toggle="tooltip"
  data-bs-placement="top"
  title="Delete"
  :style="{ cursor: isEnded ? 'not-allowed' : 'pointer' }"
>
  <i
    class="fa fa-trash fa-md"
    :class="{ 'disabled-icon': isEnded }"
    style="color: rgb(184, 38, 38)"
  ></i>
</span>
                    <span
                      @click="toggleRow(group.id)"
                      style="cursor: pointer; margin-left: 10px"
                      class="toggle-icon"
                      :class="{ expanded: expandedRows.includes(group.id) }"
                      data-bs-toggle="tooltip"
                      data-bs-placement="top"
                      title="Team details"
                    >
                      <small>
                        <i
                          class="bi bi-eye-fill"
                          :style="{
                            color: expandedRows.includes(group.id)
                              ? '#b8820f'
                              : '#242c6d',
                          }"
                        ></i>
                      </small>
                    </span>
                  </td>
                  <td>
                    <div style="margin-left: 40px; width: 5%"></div>
                  </td>
                </tr>
                <tr class="datas">
                  <td :colspan="4" v-show="expandedRows.includes(group.id)">
                    <div class="text-start mt-1">
                      <h5 v-if="group.teams.length > 0">Teams</h5>
                    </div>
                    <div class="team-names d-flex flex-wrap row gx-4 mx-2">
                      <div
                        class="col-md-3 col-lg-2 col-sm-4"
                        v-for="(team, index) in group.teams"
                        :key="index"
                      >
                        <div
                          class="d-flex justify-content-center card shadow mb-2 mt-3 py-2"
                        >
                          <div>
                            <LogoContainer
                              :showImage="true"
                              class="d-flex justify-content-center"
                              v-if="team.logo_url"
                              borderRadius="50%"
                              containerWidth="100px"
                              containerHeight="100px"
                              :imageUrl="logoUrl(team.logo_url)"
                              style="margin-inline: auto"
                            />
                            <LogoContainer
                              v-if="!team.logo_url"
                              :showImage="true"
                              class="d-flex justify-content-center"
                              borderRadius="50%"
                              containerWidth="100px"
                              containerHeight="100px"
                              :imageUrl="noImage"
                              style="margin-inline: auto"
                            />
                          </div>
                          <small
                            ><span
                              class="text-black mt-2"
                              v-b-tooltip.hover
                              :title="team.name.length > 10 ? team.name : ''"
                              >{{
                                team.name.length > 10
                                  ? truncateText(team.name, 10)
                                  : team.name
                              }}</span
                            ></small
                          >
                        </div>
                      </div>
                      <div v-if="group.teams.length === 0">
                        <img
                          :src="emptyTeams"
                          alt="Image"
                          style="margin-top: 10px; width: 150px; height: 150px"
                        /><br />
                        <p style="font-size: small">
                          {{ $t("No_teams_are_added") }}
                        </p>
                      </div>
                    </div>
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import NavBar from "./NavBar.vue";
import ButtonComponent from "@/components/Button.vue";
import LogoContainer from "@/components/LogoContainer.vue";
import image from "@/assets/img/logos/CSK_Logo.jpg";
import noImage from "@/assets/img/logos/noPic.jpg";
import { getTournamentById } from "@/services/tournamentService";
import { GroupList, removeGroup } from "@/services/groupService";
import listEmpty from "@/assets/img/empty-list-team.jpg";
import emptyTeams from "@/assets/img/logos/folder_empty.jpg";
import Swal from "sweetalert2";
export default {
  components: {
    ButtonComponent,
    NavBar,
    LogoContainer,
  },
  mounted() {
    if (this.$route?.params?.TournamentId) {
      const secret = "tournamentGroups";
      try {
        this.tournamentId = atob(this.$route?.params?.TournamentId).replace(
          secret,
          ""
        );
      } catch (error) {
        this.$router.push("not-found");
      }
    }
    this.getTournaentDetails();
    this.getGroupList();
  },
  data() {
    return {
      grouplist: [],
      expandedRows: [],
      image: image,
      noImage: noImage,
      tournamentId: "",
      isEnded: false,
      listEmpty,
      showFullText: false,
      emptyTeams,
    };
  },
  methods: {
    getTournaentDetails() {
      getTournamentById(this.tournamentId).then(
        (response) => {
          const currentDate = new Date().toISOString().split("T")[0]; //gives the date in YYYY-MM-DD without the time
          if (response.data.end_date < currentDate) {
            this.isEnded = true;
          }
        },
        () => {
          this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });
        }
      );
    },
    emptyList() {
      if (this.grouplist.length == 0) {
        return true;
      }
    },
    editGroup(groupId) {
      const secret = "editGroup";
      const encodedGroupId = btoa(groupId + secret);
      const encodedTourId = btoa(this.tournamentId + secret);
      this.$router.push({
        name: "update-group",
        params: { TournamentId: encodedTourId, groupid: encodedGroupId },
      });
    },
    deleteGroup(groupId) {
      let param = {
        tournament_id: +this.tournamentId,
        group_id: +groupId,
      };
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
          removeGroup(param).then(
            () => {
              Swal.fire({
                icon: "success",
                text: "Deleted successfully",
              }).then(() => {
                window.location.reload();
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
    toggleRow(groupId) {
      if (this.expandedRows.includes(groupId)) {
        // Row is expanded, collapse it
        this.expandedRows = this.expandedRows.filter((id) => id !== groupId);
      } else {
        // Row is collapsed, expand it
        this.expandedRows.push(groupId);
      }
    },
    addGroup() {
      const encodedId = btoa(this.tournamentId + "Addgroup");
      this.$router.push({
        name: "add-group",
        params: { TournamentId: encodedId },
      });
    },
    getGroupList() {
      GroupList(this.tournamentId).then(
        (response) => {
          this.grouplist = response.data;
        },
        (error) => {
          if (error.response.data.error_code == 1039) {
            this.$router.push("not-found");
          }
        }
      );
    },
    truncateText(text, limit) {
      if (text.length > limit) {
        return text.slice(0, limit) + "...";
      }
      return text;
    },
    logoUrl(url) {
      try {
        return require(`${process.env.VUE_APP_FILE_PATH}/${url}`);
      } catch {
        return `${process.env.VUE_APP_FILE_PATH}/${url}`;
      }
    },
  },
};
</script>
<style scoped>
.disabled-icon {
  opacity: 0.5;
}
</style>
