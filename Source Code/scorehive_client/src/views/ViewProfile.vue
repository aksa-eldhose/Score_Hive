<template>
  <NavBar />
  <div class="padding">
    <div class="container">
      <div class="row">
        <div class="col-sm-12 col-md-8 col-lg-8 mx-auto">
          <div class="card">
            <img
              class="card-img-top"
              alt="Card image cap"
              :src="cricketSignin"
            />
            <div class="card-body little-profile text-center">
              <div class="pro-img"><img :src="user_profile" alt="user" /></div>
              <div v-if="user">
                <p>{{ user.name }}</p>
                <p>{{ user.Phone_Number }}</p>
              </div>
              <button
                class="btn btn-primary ml-20"
                style="
                  width: 200px;
                  margin-top: 20px;
                  background-color: hsl(219, 44%, 32%);
                  border: none;
                "
                @click="editProfile()"
              >
                {{ $t("Edit_Profile") }}</button
              ><br />
              <router-link
                to="/ChangePassword"
                class="btn btn-success ml-30"
                style="width: 200px; margin-top: 20px"
              >
                {{ $t("Change_Password") }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import cricketSignin from "@/assets/img/cricketSignin.jpg";
import user_profile from "@/assets/img/user_profile.png";
import NavBar from "./NavBar.vue";
import { userProfile } from "@/services/authService";
export default {
  components: {
    NavBar,
  },
  mounted() {
    userProfile().then(
      (response) => {
        this.user = {
          name: response.data.Name,
          Phone_Number: response.data.Phone_Number,
        };
        localStorage.setItem("User_name", response.data.Name);
        localStorage.setItem("Phone_number", response.data.Phone_Number);
      },
      () => {
        this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });
      }
    );
  },
  data() {
    return {
      user: null,
      cricketSignin: cricketSignin,
      user_profile: user_profile,
    };
  },
  methods: {
    editProfile() {
      this.$router.push({
        name: "profile-edit",
      });
    },
  },
};
</script>
<style scoped>
body {
  background-color: #fffbfb;
}
.card-img-top {
  height: 300px;
}
.pro-img {
  margin-top: -80px;
  margin-bottom: 20px;
}
.little-profile .pro-img img {
  width: 128px;
  height: 128px;
  -webkit-box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  border-radius: 100%;
}
@media (max-width: 767px) {
  .mx-auto {
    margin-left: auto !important;
    margin-right: auto !important;
  }
}
@media (min-width: 768px) and (max-width: 1023px) {
  .mx-auto {
    margin-left: auto !important;
    margin-right: auto !important;
    width: 50%;
  }
}
@media (min-width: 1024px) and (max-width: 1280px) {
  .mx-auto {
    margin-left: auto !important;
    margin-right: auto !important;
    width: 60%;
  }
}
@media (min-width: 1281px) {
  .mx-auto {
    margin-left: auto !important;
    margin-right: auto !important;
    width: 70%;
  }
}
</style>