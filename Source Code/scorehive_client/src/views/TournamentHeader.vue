<template>
  <!-- Navigation Bar -->
  <nav class="navbar navbar-expand-lg navbar" style="background: hsl(217, 33%, 33%); height: 80px;
">
  <div>
    <ul class="navbar-nav" style="color: white; margin-left: 20px; text-decoration: none;">
      <li class="nav-item">
        <Router-link
          :to="{
            name: 'Match',
            query: { tournamentId: this.$route.query.tournamentId },
          }"
          style="color: white; text-decoration: none;  margin-left: 20px; font-size: 12px;"
        ><b>MATCHES</b>
        </Router-link>
      </li>
      <li class="nav-item">
        <Router-link
          :to="{
            name: 'PointTable',
            query: { tournamentId: this.$route.query.tournamentId },
          }"
          style="color: white;  margin-left: 20px; text-decoration: none; font-size: 12px;"
        ><b>POINT TABLE</b>
        </Router-link>
      </li>
      <li class="nav-item">
        <Router-link
          :to="{
            name: 'TournamentTeam',
            query: { tournamentId: this.$route.query.tournamentId },
          }"
          style="color: white; text-decoration: none; margin-left: 20px; font-size: 12px;"
        ><b>TEAMS</b>
        </Router-link>
      </li>
      <li class="nav-item">
        <Router-link
          :to="{
            name: 'AboutTournament',
            query: { tournamentId: this.$route.query.tournamentId },
          }"
          style="color: white; text-decoration: none; margin-left: 20px; font-size: 12px;"
        ><b>ABOUT</b></Router-link>
      </li>
    </ul>
  </div>
</nav>
</template>
<script>
import cric from "@/assets/img/cric.png";
import scorehive from "@/assets/img/logo_6.png";
import { defineComponent } from "vue";
export default defineComponent({
  name: "NavBar",
  data() {
    return {
      cric: cric,
      scorehive: scorehive,
    };
  },
  mounted() {
    this.tournamentId = atob(this.$route.query.tournamentId).replace(
      "Tournament",""
    );
  },
  components: {},
});
</script>

