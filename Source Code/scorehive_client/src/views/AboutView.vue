<template>
  <NavBar />
  <div class="about">
    <h1>{{ $t("Group-name") }}</h1>
  </div>
</template>
<script>
import { defineComponent } from "vue";
import NavBar from "./NavBar.vue";
export default defineComponent({
  name: "HomeView",
  components: {
    NavBar,
  },
  methods: {},
});
</script>
