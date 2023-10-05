<template>
  <NavBar />
  <div>
    <div class="d-flex justify-content-center">
      <div class="card shadow-lg mx-lg-5 my-lg-5 bg-white p-4 w-100 h-100">
        <div class="d-flex justify-content-between" v-if="cards">
          <h2 class="text-dark">{{ $t("Team_members") }}</h2>
          <div>
            <cbutton color="primary" class="ml-1 mt-1" @click="addPlayer">
              {{ $t("Add_Player") }}
            </cbutton>
            <cbutton
              v-if="cards.length > 0"
              type="button"
              class="btn btn-danger m-1"
              @click="removePlayer()"
              :disabled="selectedCardIds?.length === 0"
            >
              {{ $t("Delete") }}
            </cbutton>
          </div>
        </div>
        <hr />
        <div class="row"></div>
        <div class="row mt-sm-4 mx-lg-5 mx-sm-2">
          <!-- player card -->
          <div v-for="(card, index) in cards"
              :key="index" class="col-md-3 col-sm-4">
            <div
              class="card shadow m-2 p-2" 
            >
              <input
                type="checkbox"
                class="d-flex justify-content-end form-check-input"
                :class="{ selected: selectedCardIds.includes(card.player_id) }"
                @click="toggleCardSelection(card.player_id)"
              />
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
import LogoContainer from "@/components/LogoContainer.vue";
import listEmpty from "@/assets/img/empty-list-team.jpg";
import Swal from "sweetalert2";
import cbutton from "@/components/Button.vue";
import NavBar from "./NavBar.vue";
import user_profile from "@/assets/img/user_profile.png";
import { playerList, removePlayer } from "@/services/playerService";
import image from "@/assets/img/logos/tst-logo.jpg";
import noImage from "@/assets/img/logos/noImage.png";
import errorCodes from "@/services/errorCodes.json";

export default {
  components: {
    NavBar,
    cbutton,
    LogoContainer,
  },
  data() {
    return {
      user_profile: user_profile,
      listEmpty,
      image,
      noImage,
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
    addPlayer() {
      const id = this.$route.params.teamId;
      this.$router.push({
        name: "AddPlayer",
        query: { team: id },
      });
    },
    truncateText(text, limit) {
      if (text.length > limit) {
        return text.slice(0, limit) + "...";
      }
      return text;
    },
    toggleCardSelection(cardId) {
      if (this.selectedCardIds.includes(cardId)) {
        this.selectedCardIds = this.selectedCardIds.filter(
          (id) => id !== cardId
        );
        return;
      }
      this.selectedCardIds.push(cardId);
    },
    removePlayer() {
      const teamId = atob(this.$route.params.teamId).replace("Team", "");
      const selectedCards = this.selectedCardIds;
      Swal.fire({
        title: "Are you sure?",
        text: this.$t("Are_you_sure") + "..",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: this.$t("Delete"),
        cancelButtonText: this.$t("Cancel"),
      }).then((result) => {
        if (result.isConfirmed) {
          this.callRemovePlayer(teamId, selectedCards);
        }
      });
    },
    callRemovePlayer(teamId, selectedCardIds) {
      removePlayer({
        team_id: Number(teamId),
        player_ids: selectedCardIds,
      }).then(
        () => {
          Swal.fire({
            icon: "success",
            text: "Deleted successfully",
          }).then(() => {
            window.location.reload();
          });
          this.playerList();
        },
        (error) => {
          this.playerList();
          const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
          window.location.reload();
         
        }
      );
    },
  },
};
</script>
<style scoped>
.card {
  box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
}
</style>
