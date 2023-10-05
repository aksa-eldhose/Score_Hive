<template>
  <NavBar />
  <div class="position-relative overlay">
    <div class="img-card full-screen-logo">
      <div class="position-absolute top-10 left-10 w-100 h-100">
        <img :src="imageSource" :alt="imageAlt" />
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <div
          class="position-absolute top-0 left-0"
          style="margin-top: 45px; margin-left: 20px"
        >
          <div class="d-flex align-items-center">
            <LogoContainer
              :showImage="logo !== 1"
              :imageUrl="imageUrl || emptytournament"
              :emptyImageContent="emptyImageContent"
              containerWidth="150px"
              containerHeight="150px"
              borderRadius="50%"
              style="z-index: 10"
            />
          </div>

          <h4
            class="text-center ml-6 overlay-text"
            style="margin-left: 150px; margin-top: -40px"
            :title="name.length > 80 ? name : ''"
          >
            <b>{{ name.length > 80 ? name.substring(0, 80) + "..." : name }}</b>
          </h4>
        </div>
      </div>
    </div>
  </div>
  <TournamentHeader />
  <router-view></router-view>
</template>
<script>
import NavBar from "./NavBar.vue";
import emptytournament from "@/assets/img/emptylist-tournament.jpg";
import TournamentHeader from "./TournamentHeader.vue";
import "bootstrap-icons/font/bootstrap-icons.css";
import LogoContainer from "@/components/LogoContainer.vue";
import errorCodes from "@/services/errorCodes.json";
import { getTournamentDetails } from "@/services/tournamentService";
export default {
  components: {
    NavBar,
    TournamentHeader,
    LogoContainer,
  },
  mounted() {
    this.tournamentId = atob(this.$route.query.tournamentId).replace(
      "Tournament",
      ""
    );
    this.fetchTournamentDetails();
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
      flag: 0, // Initialize flag to 0
    };
  },
  methods: {
    fetchTournamentDetails() {
      getTournamentDetails(this.tournamentId).then(
        (response) => {
          this.name = response.data.name;
          this.location = response.data.city.name;
          this.start_date = response.data.start_date;
          this.end_date = response.data.end_date;
          this.ground = response.data.ground.name;
          this.match_type = response.data.match_type;
          this.ball_type = response.data.ball_type;
          this.category = response.data.tournament_type;
          try {
            if (response.data.logo_url) {
              this.imageUrl = require(`../assets${response.data.logo_url}`);
            }
          } catch (error) {
            this.imageUrl = `${process.env.VUE_APP_FILE_PATH}${response.data.logo_url}`;
          }
          try {
            if (response.data.banner_url) {
              this.flag = 1; // Set flag to 1 if banner is present
              this.bannerUrl = require(`../assets${response.data.banner_url}`);
            }
          } catch (error) {
            this.bannerUrl = `${process.env.VUE_APP_FILE_PATH}${response.data.banner_url}`;
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
    
  },
  computed: {
    imageSource() {
      // Check the flag value to determine the image source
      return this.flag === 1 ? this.bannerUrl : this.emptytournament;
    },
    imageAlt() {
      // Set the alt text based on the flag value
      return this.flag === 1 ? "Banner Image" : "Default Image";
    },
  },
};
</script>
<style scoped>
.overlay {
  position: relative;
}
.overlay::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.overlay-text {
  position: relative;
  color: white;
  z-index: 2;
}

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
  display: block;
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
