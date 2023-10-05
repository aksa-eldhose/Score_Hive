<template>
  <div class="min-vh-100 bg-light">
    <NavBar />
    <div>
      <div class="d-flex justify-content-center">
        <div class="card shadow-lg mx-lg-5 my-lg-5 bg-white p-4 w-100 h-100">
          <h2 class="text-dark">{{ $t("Add_new_group") }}</h2>
          <hr />
          <div
            v-if="this.flag === 1"
            class="fs-4 text-center justify-content-center align-items-center"
          >
            <img :src="listEmpty" alt="Image" style="margin-top: 10px" /><br />
            <p style="font-size: medium">
              {{ $t("No_teams_available_for_grouping") }}..!
            </p>
            <Button color="primary" class="m-1" @click.prevent="cancel()">
              <span>{{ $t("Go_Back") }}</span></Button
            >
          </div>
          <form v-else class="mt-lg-4 mt-sm-2">
            <div class="row my-2">
              <div class="col-md-6">
                <div class="mx-lg-5 mx-sm-2">
                  <label for="group-name"
                    ><span class="text-dark">{{
                      $t("Group_name")
                    }}</span></label
                  >
                  <input
                    type="text"
                    class="form-control"
                    id="group-name"
                    v-model.trim="name"
                    :placeholder="$t('Enter_group_name')"
                  />
                  <div
                    v-for="(error, index) of v$.name.$errors"
                    :key="index"
                    class="text-danger"
                  >
                    <span v-if="error.$params.type === 'required'"
                      ><small>{{ $t("Please_enter_your_group_name") }}</small
                      >.</span
                    >
                    <span v-if="error.$params.type === 'maxLength'"
                      ><small
                        >{{ $t("Group_name_is_too_long") }}...</small
                      ></span
                    >
                    <span v-if="error.$params.type === 'minLength'"
                      ><small
                        >{{ $t("Group_name_is_too_short") }}...</small
                      ></span
                    >
                  </div>
                </div>
              </div>
            </div>
            <div class="row mt-sm-4 mx-lg-5 mx-sm-2">
              <div>
                <span>{{ $t("Select_teams_in_this_group") }}</span
                ><br />
                <span class="text-danger"
                  ><small v-if="v$.selectedTeams.$error"
                    >{{ $t("Please_select_teams") }}..!</small
                  ></span
                >
              </div>
              <div
                v-for="(team, index) in teams"
                :key="index"
                class="col-md-3 col-sm-4"
              >
                <div class="card shadow m-2 p-2">
                  <input
                    type="checkbox"
                    :value="team.id"
                    v-model="selectedTeams"
                    class="d-flex justify-content-end form-check-input"
                  />

                  <LogoContainer
                    v-if="team.logo_url"
                    :showImage="true"
                    class="d-flex justify-content-center m-1 mx-lg-4"
                    borderRadius="50%"
                    containerWidth="100"
                    :imageUrl="logoUrl(team.logo_url)"
                  />
                  <LogoContainer
                    v-else
                    :showImage="true"
                    class="d-flex justify-content-center m-1 mx-lg-4"
                    borderRadius="50%"
                    containerWidth="100"
                    :imageUrl="noImage"
                  />

                  <span
                    class="text-black mt-2 mx-2"
                    v-b-tooltip.hover
                    :title="team.name.length > 20 ? team.name : ''"
                  >
                    {{
                      team.name.length > 15
                        ? truncateText(team.name, 15)
                        : team.name
                    }}</span
                  >
                  <small class="my-1 mx-2">
                    <i class="bi bi-geo-alt-fill text-dark">{{
                      team.city.name
                    }}</i>
                  </small>
                </div>
              </div>
            </div>
            <div class="row" style="margin-left: 4%">
              <div class="d-flex justify-content-start m-2">
                <Button
                  color="primary"
                  class="m-1"
                  :disabled="isLoading"
                  @click.prevent="submit"
                  ><span
                    v-if="isLoading"
                    class="spinner-border spinner-border-sm mx-3"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  <span v-else>{{ $t("Submit") }}</span></Button
                >
                <Button
                  color="primary"
                  variant="outline"
                  class="m-1"
                  @click.prevent="cancel()"
                  >{{ $t("Cancel") }}</Button
                >
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import NavBar from "./NavBar.vue";
import Button from "@/components/Button.vue";
import LogoContainer from "@/components/LogoContainer.vue";
import image from "@/assets/img/logos/tst-logo.jpg";
import noImage from "@/assets/img/logos/noImage.png";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength, maxLength } from "@vuelidate/validators";
import { createGroup, GroupTeamList } from "@/services/groupService";
import errorCodes from "@/services/errorCodes.json";
import listEmpty from "@/assets/img/logos/EmptyFile.png";

export default {
  name: "AddGroup",
  // eslint-disable-next-line vue/no-reserved-component-names
  components: { NavBar, Button, LogoContainer },
  setup() {
    return { v$: useVuelidate() };
  },
  data() {
    return {
      teams: [],
      selectedTeams: [],
      image: image,
      noImage: noImage,
      name: "",
      isLoading: false,
      tournamentId: "",
      listEmpty,
      flag: 2,
    };
  },
  mounted() {
    if (this.$route?.params?.TournamentId) {
      const secret = "Addgroup";
      try {
        this.tournamentId = atob(this.$route?.params?.TournamentId).replace(
          secret,
          ""
        );
      } catch (error) {
        this.$router.push("not-found");
      }
    }
    // this.tournamentId = this.$route?.params?.TournamentId
    this.fetchTeams(this.tournamentId);
  },
  validations() {
    return {
      name: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(100),
      },
      selectedTeams: {
        required,
      },
    };
  },
  methods: {
    async submit() {
      this.isLoading = true;
      const isValid = await this.v$.$validate();
      if (isValid) {
        let param = {
          tournament_id: +this.tournamentId,
          name: this.name,
          team_ids: this.selectedTeams,
        };
        createGroup(param).then(
          () => {
            this.$toast.success(this.$t("Created_successfully") + "..");
            setTimeout(() => {
              this.isLoading = false; // Set isLoading to false after a delay
            }, 1000);
            const encodedId = btoa(this.tournamentId + "tournamentGroups");
            this.$router.push({
              name: "group",
              params: { TournamentId: encodedId },
            });
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
      } else {
        this.isLoading = false;
        window.scrollTo(0, 0);
      }
    },
    cancel() {
      const encodedId = btoa(this.tournamentId + "tournamentGroups");
      this.$router.push({
        name: "group",
        params: { TournamentId: encodedId },
      });
    },
    fetchTeams(tournamentId) {
      GroupTeamList(tournamentId).then(
        (response) => {
          this.teams = response.data;
          if (this.teams.length === 0) {
            this.flag = 1;
          } else {
            this.flag = 0;
          }
        },
        () => {
          this.$toast.error("Oops!Some unknown error occured..");
        }
      );
    },
    logoUrl(url) {
      try {
        return  require(`${process.env.VUE_APP_FILE_PATH}${url}`);
      } catch {
        return `${process.env.VUE_APP_FILE_PATH}${url}`;
      }
    },
    truncateText(text, limit) {
      if (text.length > limit) {
        return text.slice(0, limit) + "...";
      }
      return text;
    },
    isListEmpty() {
      return this.teams.length === 0;
    },
  },
};
</script>
