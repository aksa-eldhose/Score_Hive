<template>
  <NavBar />
  <div>
    <div class="d-flex justify-content-center">
      <div class="card shadow-lg mx-lg-5 my-lg-5 bg-white p-4 w-100 h-100">
        <div class="d-flex justify-content-between" v-if="cards">
          <h2 class="text-dark">{{ $t("Team_members") }}</h2>
        </div>
        <hr />
        <div class="row"></div>
        <div class="row mt-sm-4 mx-lg-5 mx-sm-2">
          <!-- player card -->
          <div class="col-md-3 col-sm-4"  v-for="(card, index) in cards"
              :key="index">
            <div
              class="card shadow m-2 p-2"
            
            >
              <LogoContainer
                :showImage="user_profile"
                class="d-flex justify-content-center m-1 mx-lg-4"
                borderRadius="50%"
                containerWidth="100"
                :imageUrl="user_profile"
              />
              <div v-if="cards" style="color: black">
                <p class="card_text" :title="card.name" style="color: black">
                  {{ showFullText ? card.name : truncateText(card.name, 15) }}
                  <span v-if="!showFullText && card.name.length > 10"></span>
                </p>
                <p class="card_text" :title="card.email" style="color: black">
                  {{ showFullText ? card.email : truncateText(card.email, 20) }}
                  <span v-if="!showFullText && card.email.length > 20"></span>
                </p>
              </div>
            </div>
          </div>
        </div>
        <div v-if="this.length == 0" class="text-center">
          <h2>{{ $t("NoTeam_members") }}..!</h2>
          <img :src="listEmpty" style="margin-top: 20px" alt=""/>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import listEmpty from "@/assets/img/empty-list-team.jpg";
import NavBar from "./NavBar.vue";
import user_profile from "@/assets/img/user_profile.png";
import { playerList } from "@/services/playerService";
import LogoContainer from "@/components/LogoContainer.vue";

export default {
  components: {
    NavBar,
    LogoContainer,
  },
  data() {
    return {
      user_profile: user_profile,
      listEmpty,
      cards: [], // Array to store card data received from the backend
      selectedCardIds: [],
      showFullText: false, // Array to store selected card IDs
    };
  },
  mounted() {
    // Simulating data received from the backend
    this.playerList();
  },
  methods: {
    playerList() {
      const teamId = atob(this.$route.params.teamId).replace("Team", "");
      playerList(teamId).then(
        (response) => {
          this.cards = response.data;
          this.length = response.data.length;
        },
        () => { this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          }); }
      );
    },
    truncateText(text, limit) {
      if (text.length > limit) {
        return text.slice(0, limit) + "...";
      }
      return text;
    },
  },
};
</script>

