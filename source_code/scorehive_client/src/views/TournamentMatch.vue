<template>
  <div>
    <div class="d-flex justify-content-center m-4">
      <span class="badge square-pill bg-success" style="padding: 10px">{{
        $t("On_Going")
      }}</span
      >&nbsp;
      <span class="badge square-pill bg-warning" style="padding: 10px">{{
        $t("Upcoming")
      }}</span
      >&nbsp;
      <span class="badge square-pill bg-primary" style="padding: 10px">{{
        $t("Completed")
      }}</span>
    </div>
    <div class="d-flex flex-wrap justify-content-center">
  <div class="card m-4" style="width: 18rem" v-for="match in matchList" :key="match" @click="matchDetails">
    <h6 class="card-header mt-3 text-center">{{ match.tournament_name }}</h6>
    <div class="card-body">
  <p class="card-text"><strong>{{ match.teamA }}</strong></p>
  <p class="card-text"><strong>{{ match.teamsB }}</strong></p>
  <p class="card-text"><small>{{ match.round }}</small></p>
  <p class="card-text"><i class="bi bi-geo-alt-fill" style="color:rgb(33, 95, 211)"></i><small>{{ match.location }}</small></p>
  <p class="card-text"><i class="bi bi-calendar-date-fill" style="color:rgb(57, 151, 85)"></i>&nbsp;<small>{{ match.date_time }}</small></p>
</div>
  </div>
</div>
  </div>
</template>
<script>
export default {
  mounted() {
    this.tournamentId = atob(this.$route.query.tournamentId).replace(
      "Tournament",
      ""
    );
  },

  data() {
    return {
      tournamentId: "",
      matchList: [
        {
          id: "1",
          tournament_name: "Indian Premier League",
          location: "Abc Ground,Old Woking CC,Kochi",
          date_time: "16-Oct-23 06:30 PM",
          teamA: "Chennai Super Kings",
          teamsB: "Royal Challengers Bangalore",
          round:"Semi final"
        },
        {
          id: "2",
          tournament_name: "Indian Premier League",
          location: "Abc Ground,Old Woking CC,Kochi",
          date_time: "26-Oct-23 06:30 PM",
          teamA: "Mumbai Indians",
          teamsB: "Royal Challengers Bangalore",
          round:"Qualifier 1"
        },
        {
          id: "3",
          tournament_name: "Indian Premier League",
          location: "Abc Ground,Old Woking CC,Kochi",
          date_time: "06-Oct-23 06:30 PM",
          teamA: "Mumbai Indians",
          teamsB: "Chennai Super Kings",
          round:"Qualifier 2"
        },
        {
          id: "4",
          tournament_name: "Indian Premier League",
          location: "Abc Ground,Old Woking CC,Kochi",
          date_time: "17-Oct-23 06:30 PM",
          teamA: "Rjasthan Royals",
          teamsB: "Chennai Super Kings",
          round:"Final"
        },
        {
          id: "5",
          tournament_name: "Indian Premier League",
          location: "Abc Ground,Old Woking CC,Kochi",
          date_time: "11-Oct-23 06:30 PM",
          teamA: "Rajasthan Royals",
          teamsB: "Chennai Super Kings",
          round:"Semi Final"
        },
        {
          id: "6",
          tournament_name: "Indian Premier League",
          location: "Abc Ground,Old Woking CC,Kochi",
          date_time: "12-Oct-23 06:30 PM",
          teamA: "Lucknow Super Giants",
          teamsB: "Delhi Capitals",
          round:"Qualifier 2"
        }
      ],
    };
  },
  methods:{
    truncateText(text, limit) {
      if (text.length > limit) {
        return text.slice(0, limit) + "...";
      }
      return text;
    },
    matchDetails(){
      this.$router.push({
                name: "match-details",
              });
    }
  }
};
</script>
<style scoped>
.card {
  flex: 0 0 25%; 
  max-width: 25%;
  box-sizing: border-box;
  display: block;
  margin-bottom: 20px;
  line-height: 1.42857143;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
  transition: box-shadow 0.25s;
}
</style>