<template>
  <div class="text-center">
    <h2 class="text-start" style="margin-left: 50px; margin-top: 10px">
      Point Table
    </h2>
  </div>
</template>
<script>
export default {
  data() {
    return {};
  },
  mounted() {
    this.tournamentId = atob(this.$route.query.tournamentId).replace(
      "Tournament",
      ""
    );
  },
};
</script>
