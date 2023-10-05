<template>
  <NavBar />
  
  <section class="wrapper">
    <div class="container-fostrap">
      <div class="content">
        <div class="container">
          <div class="d-flex justify-content-between">
            <h2 class="text-start mr-auto">
              {{ $t("All Cricket Tournaments") }}
            </h2>
            <div class="search-container">
              <input
                type="text"
                placeholder="Search.."
                name="search"
                class="form-control"
              />
              <button type="btn-primary" class="search-button" @click="search">
                <i class="fa fa-search"></i>
              </button>
            </div>
          </div>
          <hr />
          <div class="row" v-if="!loading">
            <div
              v-for="(card, index) in list"
              :key="index"
              class="col-md-3 col-sm-4"
            >
              <div class="card" @click="viewTournamentDetail(card.id)">
                <a class="img-card">
                  <img
                    v-if="card.banner_url"
                    :src="getLogoUrl(card.banner_url)"
                    alt=""
                  />
                  <img v-else :src="emptytournament" alt="" />
                </a>
                <div class="card-content">
                  <div class="d-flex flex-wrap justify-content-between">
                    <h4
                      class="card-title"
                      :title="card.name.length > 6 ? card.name : ''"
                    >
                      <b>
                        {{ card.name }}
                      </b>
                    </h4>
                    <h5>
                      <span
                        v-if="card.tournament_status === 1"
                        class="badge rounded-pill bg-success"
                        >Ongoing</span
                      >
                      <span
                        v-else-if="card.tournament_status === 2"
                        class="badge rounded-pill bg-warning"
                        >Upcoming</span
                      >
                      <span v-else class="badge rounded-pill bg-primary"
                        >Completed</span
                      >
                    </h5>
                  </div>
                  <span class="social-box">
                    <i class="fa fa-map-marker"></i>
                    <span :title="card.city.name">{{
                      card.city.name.length > 8
                        ? card.city.name.substring(0, 8) + "..."
                        : card.city.name
                    }}</span
                    >,
                    <span :title="card.ground.name">{{
                      card.ground.name.length > 8
                        ? card.ground.name.substring(0, 8) + "..."
                        : card.ground.name
                    }}</span
                    ><br />

                    <i class="fa fa-calendar"></i>{{ card.start_date }} to
                    {{ card.end_date }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center">
            <div
              v-if="loading"
              class="d-flex justify-content-center align-items-center"
              style="height: 100px; margin-top: 250px"
            >
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="loading" class="progress">
      <div
        class="progress-bar progress-bar-striped progress-bar-animated"
        role="progressbar"
        aria-valuenow="100"
        aria-valuemin="0"
        aria-valuemax="100"
      ></div>
    </div>
  </section>
</template>
<script>
import NavBar from "./NavBar.vue";
import emptytournament from "@/assets/img/emptylist-tournament.jpg";
import { alltournamentList } from "@/services/tournamentService";
import errorCodes from "@/services/errorCodes.json";
import "bootstrap-icons/font/bootstrap-icons.css";

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      list: {},
      imageUrl: "",
      emptytournament,
      loading: false,
    };
  },
  mounted() {
    this.tournamentList();
  },

  methods: {
    getLogoUrl(bannerurl) {
      try {
        if (bannerurl) {
          return require(`${process.env.VUE_APP_FILE_PATH}${bannerurl}`);
        }
      } catch (error) {
        return `${process.env.VUE_APP_FILE_PATH}${bannerurl}`;
        // Handle the error (e.g., show a placeholder image or use a default logo)
      }
    },
    tournamentList() {
      this.loading = true;
      alltournamentList().then(
        (response) => {
          this.list = response.data;
          this.length = response.data.length;
          this.loading = false;
        },
        (error) => {
          this.loading = false;
          const errorMessage = errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
        }
      );
    },
    viewTournamentDetail(Id) {
      const encodedId = btoa(Id + "Tournament");
      this.$router.push({
        name: "TournamentDetail",
        query: { tournamentId: encodedId },
      });
    },
  },
};
</script>
<style scoped>
@import url(https://fonts.googleapis.com/css?family=Roboto:400,100,900);
.scroll-icon {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}
.icon-large {
  font-size: 2rem;
}
.scroll-icon:hover {
  background-color: #e9ecef;
}
html,
body {
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  height: 100%;
  width: 100%;
  background: #fff;
  font-family: "Roboto", sans-serif;
  font-weight: 400;
}

.wrapper {
  display: table;
  height: 100%;
  width: 100%;
  margin-top: 50px;
}

.container-fostrap {
  display: table-cell;
  padding: 1em;
  text-align: center;
  vertical-align: middle;
  margin-top: 50px;
}
.fostrap-logo {
  width: 100px;
  margin-bottom: 15px;
}
h1.heading {
  color: #fff;
  font-size: 1.15em;
  font-weight: 900;
  margin: 0 0 0.5em;
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
.card:hover {
  box-shadow: 0 8px 17px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}
.img-card {
  width: 100%;
  height: 150px;
  border-top-left-radius: 2px;
  border-top-right-radius: 2px;
  display: block;
  overflow: hidden;
}
.img-card img {
  width: 100%;
  height: 150px;
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
  white-space: nowrap;
  overflow: hidden !important;
  text-overflow: ellipsis;
  max-width: 165px;
}
.card-title a {
  color: #000;
  text-decoration: none !important;
}
.card-read-more {
  border-top: 1px solid #d4d4d4;
}
.card-read-more a {
  text-decoration: none !important;
  padding: 10px;
  font-weight: 600;
  text-transform: uppercase;
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
.search-container {
  display: flex;
  align-items: center;
}

.search-container input {
  width: 250px;
  height: 30px;
  font-size: 14px;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-left: 5px;
}

.search-container button {
  background-color: hsl(219, 40%, 30%);
  color: white;
  border: none;
  padding: 2px 5px;
  margin-left: 2px;
  cursor: pointer;
  border-radius: 4px;
}

.search-container button:hover {
  background-color: hsl(219, 40%, 30%);
}

.fa-search {
  font-size: 16px;
}
@media (max-width: 576px) {
  .search-container input {
    min-width: 150px;
  }
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
