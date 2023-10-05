<template>
  <div class="text-center">
    <h2 class="text-start" style="margin-left: 50px; margin-top: 10px">
      Tournament Teams
    </h2>
  </div>
  <div class="d-flex justify-content-start m-5 mt-2" v-if="this.permission==1">
    <ButtonComponent color="primary" class="m-1" @click="routes()">
      <span>Teams</span>
    </ButtonComponent>
  </div>
</template>
<script>
import { getTournamentDetails } from "@/services/tournamentService";
import ButtonComponent from "@/components/Button.vue";

export default {
  components: { ButtonComponent },
  mounted() {
    this.tournamentId = atob(this.$route.query.tournamentId).replace(
      "Tournament",
      ""
    );
    this.fetchTournamentDetails();
  },
  data() {
    return {
      permission: "  ",
    };
  },
  methods: {
    fetchTournamentDetails() {
      getTournamentDetails(this.tournamentId).then(
        (response) => {
          this.permission = response.data.permission;
        },
        () => {
          this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });
        }
      );
    },
    routes(){
      this.$router.push({
        name: "CreateTeam"
      });
    },
  },
};
</script>
