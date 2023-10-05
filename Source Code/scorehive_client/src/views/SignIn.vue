<template>
  <meta
    http-equiv="Cache-Control"
    content="no-cache, no-store, must-revalidate"
  />
  <meta http-equiv="Pragma" content="no-cache" />
  <meta http-equiv="Expires" content="0" />
  <section
    class="min-vh-100 position-relative background-radial-gradient overflow-hidden"
  >
    <div
      class="position-absolute top-0 start-0 mt-6 text-white fw-bold text-center"
    >
      <img style="width: 200px" :src="scorehive" alt="Image" />
    </div>
    <div class="d-flex align-items-center">
      <div
        class="container px-4 py-5 px-md-5 text-center text-lg-start my-5 max-vh-80"
      >
        <div class="row gx-lg-5 align-items-center mb-5">
          <div class="col-lg-6 mb-5 mb-lg-0" style="z-index: 10">
            <h1
              class="my-5 display-5 fw-bold ls-tight"
              style="color: hsl(218, 81%, 95%)"
            >
              The best way <br />
              <span style="color: hsl(218, 81%, 75%)"
                >to manage your games</span
              >
            </h1>
            <p class="mb-4 opacity-70" style="color: hsl(218, 81%, 85%)">
              A complete solution to manage your cricket tournaments and matches
            </p>
          </div>
          <div class="col-lg-6 mb-5 mb-lg-0 position-relative">
            <div id="radius-shape-1" class="position-absolute shadow-5-strong">
              <img style="width: 300px" :src="cric" alt="" />
            </div>
            <GlassCard class="mx-lg-5 mx-sm-0 shadow-lg">
              <div class="card-body px-4 px-md-5">
                <form>
                  <div class="row">
                    <div class="col-md-12 mb-4">
                      <h2 class="text-opacity-75">Sign In</h2>
                      <h7 style="color: ">welcome back..!</h7>
                    </div>
                  </div>
                  <!-- Email input -->
                  <div class="form-floating">
                    <input
                      type="email"
                      class="form-control"
                      id="floatingEmail"
                      placeholder="name@example.com"
                      v-model.trim="email"
                    />
                    <label class="form-label text-muted" for="floatingEmail"
                      >Email address</label
                    >
                  </div>
                  <div v-if="v$.email.$errors.length == 0" class="pb-3"></div>
                  <div v-for="(error, index) in v$?.email?.$errors" :key="index" class="error">
                    <span v-if="error.$params.type == 'required'"
                      >Please enter your email.</span
                    >
                    <span v-if="error.$params.type == 'email'"
                      >Please enter a valid email</span
                    >
                  </div>
                  <!-- Password input -->
                  <div class="vh-50 form-floating">
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      id="floatingPassword"
                      placeholder="Password"
                      v-model.trim="password"
                    />
                    <label class="form-label text-muted" for="floatingPassword"
                      >Password</label
                    >
                  </div>
                  <div v-for="(error, index) in v$.password.$errors" :key="index" class="error">
                    <span v-if="error.$params.type === 'required'"
                      >Please enter your password.</span
                    >
                    <span v-if="error.$params.type == 'maxLength'"
                      >Password is too long...</span
                    >
                  </div>
                  <div
                    v-if="v$.password.$errors.length == 0"
                    class="mb-4"
                  ></div>
                  <div class="form-check mb-3">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      id="flexCheckDefault"
                      v-model="showPassword"
                    />
                    <label class="form-check-label" for="flexCheckDefault">
                      <small>Show password</small>
                    </label>
                  </div>
                  <!-- Submit button -->
                  <cbutton
                    class="mb-4 py-3"
                    fullWidth
                    variant="gradient"
                    color="primary"
                    :disabled="isLoading"
                    @click.prevent="submit()"
                    ><span
                      v-if="isLoading"
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                      aria-hidden="true"
                    ></span>
                    <span v-else class="fw-bold">Log in</span></cbutton
                  >
                </form>
                <div class="d-flex justify-content-between">
                  <RouterLink
                    :to="{ name: 'SendEmailResetPassword' }"
                    class="text-sm ml-2 mr-2 text-blue-900 cursor-pointer"
                  >
                    <small>Forgot Password..?</small>
                  </RouterLink>
                  <RouterLink
                    :to="{ name: 'register-email' }"
                    class="text-sm ml-2 mr-2 text-blue-900 cursor-pointer"
                  >
                    <small>Register</small>
                  </RouterLink>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </div>
    <P
      class="position-absolute bottom-0 start-50 translate-middle-x fs-7 text-white p-2"
    >
      © 2023 ScoreHive
    </P>
  </section>
</template>
<style scoped>
.text-blue-900 {
  color: hsl(219, 50%, 23%);
}

.text-blue-900:hover {
  color: hsl(219, 100%, 43%);
}

#radius-shape-1 {
  border-radius: 38% 62% 63% 37% / 70% 33% 67% 30%;
  bottom: -60px;
  right: -110px;
  width: 300px;
  height: 300px;
  background-color: #3d006b00;
  overflow: hidden;
}
</style>

<script>
import cric from "@/assets/img/cric.png";
import scorehive from "@/assets/img/logo_6.png";
import errorCodes from "@/services/errorCodes.json";
import { login } from "@/services/authService";
import { useVuelidate } from "@vuelidate/core";
import { required, email, maxLength } from "@vuelidate/validators";
import cbutton from "@/components/Button.vue";
import GlassCard from "@/components/GlassCard.vue";

export default {
  components: {
    cbutton,
    GlassCard,
  },
  setup() {
    return { v$: useVuelidate() };
  },
  beforeRouteLeave(to, from, next) {
    if (to.name === "verify-ResetPassword") {
      // Prevent the navigation to the email verification page
      next(false);
    } else {
      // Allow the navigation to proceed
      next();
    }
  },
  name: "SignIn",
  data() {
    return {
      email: "",
      password: "",
      isLoading: false,
      cric: cric,
      scorehive: scorehive,
      showPassword: false,
    };
  },
  validations() {
    return {
      email: {
        required,
        email,
        maxLength: maxLength(100),
      },
      password: {
        required,
        maxLength: maxLength(20),
      },
    };
  },
  methods: {
    async submit() {
      const isValid = await this.v$.$validate();
      if (isValid) {
        this.isLoading = true;
        login(this.$data).then(
          (res) => {
            localStorage.setItem("Access_Token", res.data.Access_Token);
            localStorage.setItem("Refresh_Token", res.data.Refresh_Token);
            this.$toast.show("Login Success", {
              type: "success",
            });
            this.$router.push({ name: "Home" });
          },
          (err) => {
            const errorMessage =
              errorCodes[err.response.data.error_code] ||
              "Oops.. Some unknown error occurred..!";
            this.$toast.show(errorMessage, {
              type: "error",
            });
            this.$data.email = "";
            this.$data.password = "";
            this.v$.$reset();
            this.isLoading = false;
          }
        );
      } else {
        this.isLoading = false;
      }
    },
  },
};
</script>
