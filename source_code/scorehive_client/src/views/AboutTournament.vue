<template>
  <h3
    class="text-start"
    style="margin-right: 15px; margin-top: 10px; margin-left: 40px"
  >
    Tournament Detail's
  </h3>
  <div
    class="card"
    style="margin-right: 15px; margin-top: 10px; margin-left: 40px"
  >
    <div class="card-content">
      <h4 class="card-title" :title="name.length > 22 ? name : ''">
        {{ name.length > 25 ? name.substring(0, 22) + "..." : name }}
      </h4>
      <hr />
      <span class="social-box">
        <em class="fa fa-map-marker"></em>
        &nbsp;
        <span :title="location">{{
          location.length > 20 ? location.substring(0, 20) + "..." : location
        }}</span
        >,
        <span :title="ground">{{
          ground.length > 10 ? ground.substring(0, 10) + "..." : ground
        }}</span>
        <hr />
        <em class="fa fa-calendar"></em> &nbsp;{{ start_date }} to
        {{ end_date }}</span
      >
      <hr />
      <h6>
        Tournament Category:<span
          v-if="tournament_type === 0"
          class="badge rounded-pill bg-success"
          style="margin-right: 15px; margin-top: 10px; margin-left: 20px"
          >Open</span
        >
        <span v-if="tournament_type === 1" class="badge rounded-pill bg-warning"
          >Corporate</span
        >
        <span v-if="tournament_type === 2" class="badge rounded-pill bg-primary"
          >School</span
        >
      </h6>
      <hr />

      <h6>
        Match Type:<span
          v-if="match_type === 0"
          class="badge rounded-pill bg-success"
          style="margin-right: 15px; margin-top: 5px; margin-left: 20px"
          >Limited</span
        >
        <span v-else class="badge rounded-pill bg-warning">Test</span>
      </h6>
      <hr />

      <h6>
        Ball Type:
        <span
          v-if="ball_type === 0"
          class="badge rounded-pill bg-success"
          style="margin-right: 15px; margin-top: 5px; margin-left: 5px"
          >Tennis</span
        >
        <span v-if="ball_type === 1" class="badge rounded-pill bg-warning"
          >Leather</span
        >
        <span v-if="ball_type === 2" class="badge rounded-pill bg-primary"
          >Other</span
        >
      </h6>
      <hr />
    </div>
  </div>
</template>
<script>
import errorCodes from "@/services/errorCodes.json";
import { userProfile } from "@/services/authService";
import emptytournament from "@/assets/img/emptylist-tournament.jpg";
import "bootstrap-icons/font/bootstrap-icons.css";
import { getTournamentDetails } from "@/services/tournamentService";
import Swal from "sweetalert2";
export default {
  mounted() {
    this.tournamentId = atob(this.$route.query.tournamentId).replace(
      "Tournament",
      ""
    );
    this.fetchTournamentDetails();
    this.getDetail();
  },
  data() {
    return {
      emptytournament,
      tournamentId: "",
      name: "",
      location: "",
      start_date: "",
      end_date: "",
      ground: "",
      imageUrl: "",
      bannerUrl: "",
      match_type: "",
      ball_type: "",
      category: "",
      logo_url: "",
      banner_url: "",
      tournament_type: "",
      organiser_name: "",
      contact: "",
      loading: false,
    };
  },
  methods: {
    fetchTournamentDetails() {
      this.loading = true;
      getTournamentDetails(this.tournamentId).then(
        (response) => {
          this.name = response.data.name;
          this.location = response.data.city.name;
          this.start_date = response.data.start_date;
          this.end_date = response.data.end_date;
          this.ground = response.data.ground.name;
          this.match_type = response.data.match_type;
          this.ball_type = response.data.ball_type;
          this.tournament_type = response.data.tournament_type;
          if (response.data.logo_url) {
            this.$data.imageUrl = require(`../assets${response.data.logo_url}`);
          }
          if (response.data.banner_url) {
            this.$data.bannerUrl = require(`../assets${response.data.banner_url}`);
          }
          this.loading = false;
        },
        (error) => {
          this.loading = false;
          const errorMessage =
            errorCodes[error.response?.data?.error_code] ||
            "Some unknown error occurred..!";
          Swal.fire({ icon: "error", title: "Oops...", text: errorMessage });
        }
      );
    },
    getDetail() {
      this.organiser_name = localStorage.getItem("User_name");
      this.contact = localStorage.getItem("Phone_number");
      userProfile().then(
        (res) => {
          this.organiser_name = res.data.Name;
          this.contact = res.data.Phone_Number;
          localStorage.setItem("User_name", res.data.Name);
          localStorage.setItem("Phone_number", res.data.Phone_Number);
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
  },
};
</script>
<style scoped>
.edit-icon {
  width: 25px;
  height: 25px;
  background-color: #274e96;
  color: white;
  border-radius: 50%;
}

.delete-icon {
  width: 25px;
  height: 25px;
  border-radius: 50%;
}
.card {
  display: flex;
  width: 500px;
  margin-bottom: 20px;
  line-height: 1.42857143;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
  transition: box-shadow 0.25s;
}
.img-card {
  width: 100%;
  height: 200px;
  border-top-left-radius: 2px;
  border-top-right-radius: 2px;
  display: block;
  overflow: hidden;
}
.img-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  transition: all 0.25s ease;
}
.card-content {
  padding: 15px;
  text-align: left;
}
.card-title {
  margin-top: 0px;
  font-weight: 700;
  font-size: 1.65em;
}
.card-title a {
  color: #000;
  text-decoration: none !important;
}

.social-box i {
  border: 0px solid #006eff;
  color: #006eff;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  line-height: 30px;
}

.social-box a {
  margin: 0 5px;
}

@media (min-width: 450px) {
  h1.heading {
    font-size: 3.55em;
  }
}
@media (min-width: 760px) {
  h1.heading {
    font-size: 3.05em;
  }
}
@media (min-width: 900px) {
  h1.heading {
    font-size: 3.25em;
    margin: 0 0 0.3em;
  }
}
</style>
