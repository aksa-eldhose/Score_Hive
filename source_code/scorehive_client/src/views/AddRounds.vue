<template>
  <div class="min-vh-100 bg-white">
    <NavBar />

    <div class="d-flex justify-content-center w-100 h-100">
      <div
        class="card shadow-md mx-md-5 py-md-4 my-md-5 bg-white p-2 w-100 h-100"
      >
        <h2 class="text-dark m-2">Add round</h2>
        <hr />

        <div
          class="d-flex justify-content-start align-items-center m-3"
          style="width: 600px"
        >
          <div class="col-auto" style="margin-left: 50px">
            <h5 for="roundType" class="me-2 fs-4">Round Type:</h5>
          </div>
          <select
            class="form-select form-select-md flex-grow-1"
            v-model="selectedRoundType"
            id="roundType"
          >
            <option value="roundRobin">Round Robin</option>
            <option value="knockOut">Knock Out</option>
          </select>
        </div>

        <form class="mt-lg-8 mt-sm-4 w-80">
          <div
            v-if="selectedRoundType === 'roundRobin'"
            class="row mt-sm-8 px-lg-5 mx-sm-2 w-100 gy-4 align-items-center justify-content-start card-grid"
          >
            <div
              v-for="(round, index) in RoundRobin"
              :key="index"
              class="col-md-4 col-sm-4 col-lg-2"
            >
              <div
                class="card shadow text-center square-card"
                :class="{ 'selected-card': isSelected(round.id) }"
                @click="toggleSelection(round.id)"
              >
                <span class="text-black mt-n4 mx-2 font-weight-bold">{{
                  round.name
                }}</span>
              </div>
            </div>
          </div>
          <div
            v-if="selectedRoundType === 'knockOut'"
            class="row mt-sm-8 px-lg-5 mx-sm-2 w-100 gy-4 align-items-center justify-content-start card-grid"
          >
            <div
              v-for="(knockout, index) in KnockOut"
              :key="index"
              class="col-md-4 col-sm-4 col-lg-2"
            >
              <div
                class="card shadow text-center square-card"
                :class="{ 'selected-card': isSelected(knockout.id) }"
                @click="toggleSelection(knockout.id)"
              >
                <span class="text-black mt-n4 mx-2 font-weight-bold">{{
                  knockout.name
                }}</span>
              </div>
            </div>
          </div>
          <div class="row mt-sm-4 mx-lg-5 mx-sm-2">
            <div class="d-flex justify-content-start m-2 mt-2">
              <Button
                color="primary"
                class="m-1"
                :disabled="isLoading"
                @click.prevent="submit"
              >
                <span
                  v-if="isLoading"
                  class="spinner-border spinner-border-sm mx-3"
                  role="status"
                  aria-hidden="true"
                ></span>
                <span v-else>Add Round</span>
              </Button>
              <Button
                color="primary"
                variant="outline"
                class="m-1"
                @click.prevent="cancel()"
              >
                {{ $t("Cancel") }}
              </Button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<style scoped>
.card-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.card {
  box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
}
.square-card {
  width: 100%;
  padding-bottom: 15%;
  padding-top: 15%;
  /* Additional styling as per your requirements */
}

.selected-card {
  background-color: hsla(218, 51%, 53%, 0.4);
}
</style>
<script>
import NavBar from "./NavBar.vue";
import Button from "@/components/Button.vue";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";
import image from "@/assets/img/logos/CSK_Logo.jpg";
import errorCodes from "@/services/errorCodes.json";
import noImage from "@/assets/img/logos/noImage.png";
import {
  addRound,
  roundList,
  tournamentRoundList,
} from "@/services/roundService";
import Swal from "sweetalert2";

export default {
  name: "ListRounds",
  // eslint-disable-next-line vue/no-reserved-component-names
  components: { NavBar, Button },
  setup() {
    return { v$: useVuelidate() };
  },
  data() {
    return {
      image: image,
      noImage: noImage,
      selectedRoundType: "roundRobin",
      RoundRobin: [],
      KnockOut: [],
      tournamentRound: [],
      selectedround: [],
      isLoading: false,
    };
  },
  validations() {
    return {
      selectedround: {
        required,
      },
    };
  },

  mounted() {
    this.roundList();
    this.tournamentRounds();
  },
  methods: {
    roundList() {
      roundList().then(
        (response) => {
          for (const obj of response.data) {
            if (Object.prototype.hasOwnProperty.call(obj, "round_robin")) {
              this.RoundRobin = obj.round_robin;
              break;
            }
          }

          for (const obj of response.data) {
            if (Object.prototype.hasOwnProperty.call(obj, "knock_out")) {
              this.KnockOut = obj.knock_out;
              break;
            }
          }

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
    tournamentRounds() {
      const TournamentId = atob(this.$route.params.TournamentId).replace(
        "tournamentRounds",
        ""
      );
      tournamentRoundList(TournamentId).then(
        (response) => {
          this.tournamentRound = response.data;
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
    isSelected(round) {
      return this.selectedround.includes(round);
    },
    toggleSelection(round) {
      if (this.isSelected(round)) {
        this.selectedround = this.selectedround.filter((t) => t !== round);
      } else {
        this.selectedround.push(round);
      }
    },
    async submit() {
      this.isLoading = true;
      const id = atob(this.$route.params.TournamentId).replace(
        "tournamentRounds",
        ""
      );
      const selectrdRounds = this.selectedround;
      let data = {
        tournament_id: +id,
        round_ids: selectrdRounds,
      };
      const isValid = await this.v$.$validate();
      if (isValid) {
        this.isLoading = true;
        addRound(data).then(
          () => {
            this.$toast.success(this.$t("Round added") + "..");
            this.resetSelection(); // Reset the selection
            this.cancel();
          },
          (err) => {
            this.isLoading = false;
            const errorMessage =
              errorCodes[err.response.data.error_code] ||
              "Oops.. Some unknown error occurred..!";
            Swal.fire({
              icon: "error",
              title: "Failed",
              text: errorMessage,
            });
          }
        );
      } else {
        this.isLoading = false;
        this.$toast.error("No rounds selected..");
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
    },
    resetSelection() {
      this.selectedround = [];
    },
    cancel() {
      this.$router.push({
        name: "list-rounds",
        params: { TournamentId: this.$route?.params?.TournamentId },
      });
    },
  },
};
</script>
