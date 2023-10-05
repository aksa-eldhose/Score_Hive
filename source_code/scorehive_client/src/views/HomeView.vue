<template>
  <NavBar />
</template>
<script>
import { defineComponent } from "vue";
import NavBar from "./NavBar.vue";
// Components
export default defineComponent({
  name: "HomeView",
  components: {
    NavBar,
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push({ name: "SignIn" });
    },
    myProfile() {
      this.$router.push({
        name: "View-profile",
      });
    },
  },
});
</script>
