<template>
  <NavBar />
  <div class="background-radial-gradient min-vh-100" style="min-width: 400px">
    <div
      class="d-flex align-items-center justify-content-center container min-vh-100"
    >
      <div class="row w-100">
        <div class="d-flex col-md-6 align-items-center">
          <div class="text-center">
            <h4 class="text-white">
              {{ $t("Scan_this_QR_to_join_the_team") }}
            </h4>
            <div v-if="qrCode" class="qr-code-container">
              <LogoContainer
                :showImage="qrCode"
                :imageUrl="qrCode"
                :emptyImageContent="emptyImageContent"
                containerWidth="200px"
                containerHeight="200px"
                borderRadius="5%"
              />
            </div>
            <h3 class="text-white mt-5">{{ $t("OR") }}</h3>
            <br />
            <h4 class="text-white">{{ $t("Share_this_link") }}</h4>
            <h6 class="text-info">{{ link }}</h6>
            
          </div>
        </div>
        <div class="col-md-6 d-flex justify-content-center align-items-start">
          <div class="card bg-glass shadow-lg px-4 py-4">
            <div class="mb-3">
              <h6 class="mb-3">{{ $t("Add_players_to") }} {{ teamName }}</h6>
              <form @submit.prevent="">
                <div class="input-group rounded bg-white">
                  <input
                    type="search"
                    class="form-control border-0"
                    placeholder="Search email"
                    aria-label="Search"
                    aria-describedby="search-addon"
                    v-model.trim="searchTerm"
                  />
                  <Button
                    class="input-group-text text-white-50 border-0"
                    id="search-addon"
                    color="primary"
                    size="md"
                    @click="search"
                  >
                    <i class="fa fa-search"></i
                  ></Button>
                </div>
                <span
                  class="text-danger"
                  v-for="(error, index) of v$.$errors"
                  :key="index"
                  ><small v-if="error.$params.type == 'maxLength'"
                    >{{ $t("Search_term_is_too_long") }}...</small
                  ></span
                >
              </form>
            </div>
            <div class="overflow-auto" style="max-height: 60vh">
              <div v-for="(user, index) in users" :key="index">
                <div v-if="user" class="d-flex card mb-2 shadow-lg">
                  <div class="card-body d-flex justify-content-between">
                    <div>
                      <h6 :title="user.name.length > 20 ? user.name : ''">
                        {{ truncate(user.name, 20) }}
                      </h6>
                      <div class="card-email">
                        <span
                          class="card-title"
                          :title="user.email.length > 20 ? user.email : ''"
                        >
                          {{ truncate(user.email, 20) }}
                        </span>
                      </div>
                    </div>
                    <button
                      @click="addPlayer(user.id)"
                      :disabled="isLoading"
                      class="btn btn-primary ms-2"
                    >
                      <span
                        v-if="isLoading && selectedPlayerId === user.id"
                        class="spinner-border spinner-border-sm mx-2"
                        role="status"
                        aria-hidden="true"
                      ></span>
                      <span v-else>{{ $t("Add") }}</span>
                    </button>
                  </div>
                </div>
              </div>
              <div v-if="noUser === 0 && !isSearchValid" class="text-black-50">
                <hr />
                <span class="text-danger" v-if="msg">{{
                  $t("Player_is_already_member")
                }}</span>
                <span v-else>{{ $t("No_users_found") }}</span>
              </div>
              <div v-if="users.length == 0 && isSearchValid">
                <span class="text-black-50 mb-1"
                  ><small>{{
                    $t("Maybe_this_user_is_not_registered_yet")
                  }}</small></span
                >
                <div class="card mb-2">
                  <div
                    class="card-body d-flex justify-content-between align-items-center"
                  >
                    <div>
                      <div class="card-email">
                        <h6
                          class="card-title"
                          :title="searchEmail.length > 20 ? searchEmail : ''"
                        >
                          {{ truncate(searchEmail, 20) }}
                        </h6>
                      </div>
                    </div>
                    <button
                      @click="invitePlayer(searchEmail)"
                      :disabled="isLoading"
                      class="btn btn-primary ms-2"
                    >
                      <span
                        v-if="isLoading"
                        class="spinner-border spinner-border-sm mx-3"
                        role="status"
                        aria-hidden="true"
                      ></span>
                      <span v-else>{{ $t("Invite") }}</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.qr-code-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}
</style>
<script>
import { useVuelidate } from "@vuelidate/core";
import NavBar from "./NavBar.vue";
import { required, email, maxLength } from "@vuelidate/validators";
import QRCode from "qrcode";
import errorCodes from "@/services/errorCodes.json";
import {
  searchPlayer,
  invitePlayer,
  addPlayer,
} from "@/services/playerService";
import Swal from "sweetalert2";
import Button from "@/components/Button.vue";
import LogoContainer from "@/components/LogoContainer.vue";
import { getTeamDetail } from "@/services/teamService";
export default {
  name: "AddPlayer",
  components: {
    NavBar,
    // eslint-disable-next-line vue/no-reserved-component-names
    Button,
    LogoContainer,
  },
  setup() {
    return { v$: useVuelidate() };
  },
  data() {
    return {
      searchTerm: "",
      searchEmail: "",
      users: "",
      isSearchValid: false,
      link: "",
      qrCode: null,
      isLoading: false,
      invalid: false,
      teamId: "",
      noUser: 1,
      selectedPlayerId: "",
      teamName: "",
      msg: false,
      msg2: false,
    };
  },
  validations() {
    return {
      searchTerm: {
        required,
        email,
        maxLength: maxLength(100),
      },
    };
  },
  computed: {},
  methods: {
    getDetail(id) {
      getTeamDetail(+id).then(
        (res) => {
          this.teamName = res.data.name;
        },
        (err) => {
          this.$router.push("not-found");
          const errorMessage =
            errorCodes[err.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
        }
      );
    },
    truncate(text, maxLength) {
      if (text.length > maxLength) {
        return text.slice(0, maxLength) + "...";
      }
      return text;
    },
    filteredUsers() {
      if (this.searchTerm) {
        searchPlayer({ email: this.searchTerm, team_id: +this.teamId }).then(
          (res) => {
            this.users = res.data.message;
            this.noUser = 1;
            this.msg = false;
            this.msg2=false;
            try {
              if(res.data.message){
                this.isSearchValid=false
                this.msg2=true;
                this.noUser = 0;
              }
            } catch (error) {
              this.$toast.show(" Oops.. Some unknown error occurred..!", {
            type: "error",
          });
            }
          },
          (err) => {
            this.users = [];
            this.noUser = 0;
            if (err.response.data.error_code == 1027) {
              this.isSearchValid = false;
              this.msg = true;
            } else {
              this.msg = false;
            }
          }
        );
      } else {
        this.noUser = 1;
      }
    },
    search() {
      this.v$.$touch();
      this.invalid = this.v$.$invalid;
      this.isSearchValid = false;
      this.filteredUsers();

      if (!this.invalid) {
        this.isSearchValid = true;
        this.searchEmail = this.searchTerm;
      }
    },
    addPlayer(playerId) {
      this.selectedPlayerId = playerId;
      const data = {
        team_id: +this.teamId,
        player_id: playerId,
        team_join_link: this.link,
      };
      this.isLoading = true;
      addPlayer(data).then(
        async () => {
          this.$toast.show("Invited to the team via email", {
            type: "success",
          });
          await new Promise((resolve) => setTimeout(resolve, 1000));
          this.isLoading = false;
        },
        async (err) => {
          if (err.response.data.error_code == 1044) {
            Swal.fire({
              icon: "error",
              text: "Oops...This player is not available in the selected date",
            }).then(() => {
              this.isLoading = false;
            });
          } else {
            const errorMessage =
              errorCodes[err.response.data.error_code] ||
              "Oops.. Some unknown error occurred..!";
            this.$toast.show(errorMessage, {
              type: "error",
            });
            await new Promise((resolve) => setTimeout(resolve, 1000));
            this.isLoading = false;
          }
        }
      );
    },
    invitePlayer(email) {
      this.isLoading = true;
      let id = this.teamId;
      const data = { email: email, team_id: +id };
      invitePlayer(data).then(
        () => {
          Swal.fire({
            icon: "success",
            text: "Invitation sent.",
          }).then(() => {
            this.isLoading = false;
          });
        },
        (err) => {
          const errorMessage =
            errorCodes[err.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          Swal.fire({
            icon: "error",
            title: "Failed",
            text: errorMessage,
          });
          this.isLoading = false;
        }
      );
    },
    generateQRCode() {
      let id = this.$route?.query?.team;
      if (!id) {
        this.$router.push("not-found");
        return;
      }
      // eslint-disable-next-line no-undef
      this.link = process.env.VUE_APP_BASE_URL + "/join-team?team=" + id;
      if (this.link) {
        QRCode.toDataURL(this.link)
          .then((url) => {
            this.qrCode = url;
          })
          .catch((error) => {
            const errorMessage =
              errorCodes[error.response.data.error_code] ||
              "Oops.. Some unknown error occurred..!";
            this.$toast.show(errorMessage, {
              type: "error",
            });
          });
      }
    },
  },
  created() {
    if (this.$route?.query?.team) {
      const secret = "Team";
      try {
        const id = atob(this.$route?.query?.team).replace(secret, "");
        this.teamId = id;
      } catch (error) {
        this.$router.push("not-found");
      }
    }
    this.getDetail(this.teamId);
    this.generateQRCode();
  },
};
</script>
