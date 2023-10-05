<template>
  <NavBar />
  <div v-if="!member" class="background-radial-gradient w-100">
    <div class="container min-h-100">
      <div class="row min-vh-100">
        <div class="col-md-6 d-flex justify-content-center align-items-center">
          <div class="text-center">
            <h4 class="text-white mt-5 pb-2">{{ team.name }}</h4>
            <div class="d-flex justify-content-center">
              <LogoContainer
                v-if="logo"
                showImage="true"
                :imageUrl="logo"
                containerWidth="150px"
                containerHeight="150px"
                borderRadius="50%"
              /><LogoContainer
                v-else
                showImage="true"
                :imageUrl="noImage"
                emptyImageContent="NO LOGO"
                containerWidth="150px"
                containerHeight="150px"
                borderRadius="50%"
              />
            </div>
            <h6 class="text-white mt-5">
              <span style="display: inline-flex">
                <i class="bi bi-geo-alt-fill text-light"> {{ city.name }}</i>
              </span>
            </h6>
          </div>
        </div>
        <div class="col-md-6 d-flex justify-content-center align-items-center">
          <div class="card bg-glass shadow-lg px-5 py-4">
            <h5 class="mb-3">Team members</h5>
            <div class="mb-3" style="max-height: 50vh">
              <div
                v-if="players.length > 0"
                class="mb-3 mt-2 overflow-auto"
                style="max-height: 250px"
              >
                <div v-for="player of players" :key="player">
                  <span class="tag-cloud me-2">{{ player.name }}</span>
                </div>
              </div>
              <div v-else>No players in this team yet</div>
              <cbutton class="mt-4" color="primary" size="md" @click="joinTeam"
                >Join</cbutton
              >
              <cbutton
                class="mt-4 ms-2"
                variant="outline"
                color="primary"
                size="md"
                @click="cancel"
                >Cancel</cbutton
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else></div>
</template>

<style scoped>
.tag-cloud {
  display: inline-block;
  color: hsl(218, 41%, 15%);
  padding: 8px 20px;
  border-radius: 25px;
  border: 1px solid #ccc;
  border-color: hsla(220, 32%, 39%, 0.801);
  margin-top: 8px;
}
</style>

<script>
import noImage from "@/assets/img/logos/noImage.png";
import test from "@/assets/img/logos/tst-logo.jpg";
import {
  playerList,
  playerCheck,
  playerJoinTeam,
} from "@/services/playerService";
import { getTeamDetail } from "@/services/teamService";
import errorCodes from "@/services/errorCodes.json";
import NavBar from "./NavBar.vue";
import Swal from "sweetalert2";
import cbutton from "@/components/Button.vue";
import LogoContainer from "@/components/LogoContainer.vue";

export default {
  name: "JoinTeam",
  components: {
    NavBar,
    cbutton,
    LogoContainer,
  },
  data() {
    return {
      imageUrl: test,
      team: "",
      logo: false,
      players: "",
      city: "",
      errorMessage: "",
      member: false,
      teamId: "",
      noImage: noImage,
    };
  },
  mounted() {
    this.check();
  },
  methods: {
    check() {
      if (this.$route?.query?.team) {
        const secret = "Team";
        const id = atob(this.$route?.query?.team).replace(secret, "");
        this.teamId = id;
      }
      const data = {
        team_id: +this.teamId,
      };
      playerCheck(data).then(
        () => {
          this.getPlayers();
          this.getDetail();
        },
        (err) => {
          const status = err.response.status;
          const code = err.response.data.error_code;
          switch (status) {
            case 400:
              switch (code) {
                case 1025:   case 4012:  case 4015:
                  this.errorMessage =
                    errorCodes[err.response.data.error_code] ||
                    "Oops.. Some unknown error occurred..!";
                  this.$router.push("not-found");
                  break;
                case 1027:
                  this.errorMessage =
                    errorCodes[err.response.data.error_code] ||
                    "Oops.. Some unknown error occurred..!";
                  this.member = true;
                  Swal.fire({
                    icon: "warning",
                    text: "You are already a member of this team..!",
                  }).then(() => {
                    window.location.replace("/team-list");
                  });
                  break;
                default:
                  break;
              }
              break;
            case 409: case 404:
              switch (code) {
                case 1027:
                  this.errorMessage =
                    errorCodes[err.response.data.error_code] ||
                    "Oops.. Some unknown error occurred..!";
                  this.member = true;
                  Swal.fire({
                    icon: "warning",
                    text: "You are already a member of this team..!",
                  }).then(() => {
                    window.location.replace("/team-list");
                  });
                  break;
                default:
                  break;
              }
              break;
            default:
              break;
          }
        }
      );
    },
    getPlayers() {
      let id = this.teamId;
      playerList(+id).then(
        (res) => {
          this.players = res.data;
        },
        (err) => {
          this.errorMessage =
            errorCodes[err.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
        }
      );
    },
    getDetail() {
      let id = this.teamId;
      getTeamDetail(+id).then((res) => {
        this.team = res.data;
        try {
          if (res.data.logo_url) {
            this.logo = require(`${process.env.VUE_APP_FILE_PATH}${res.data.logo_url}`);
          }
        } catch (error) {
          this.logo = `${process.env.VUE_APP_FILE_PATH}${res.data.logo_url}`;
        }
        this.city = res.data.city;
      });
    },
    joinTeam() {
      const data = {
        team_id: +this.team.id,
      };

      playerJoinTeam(data).then(
        () => {
          Swal.fire({
            icon: "success",
            text: "You are now a team member",
          }).then(() => {
            window.location.replace("/team-list");
          });
        },
        (err) => {
          this.errorMessage =
            errorCodes[err.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          Swal.fire({
            icon: "error",
            text: "Oops.. Cannot join team..!",
          }).then(() => {
            window.location.replace("/team-list");
          });
        }
      );
    },
    cancel() {
      this.$router.push("/home");
    },
  },
};
</script>
