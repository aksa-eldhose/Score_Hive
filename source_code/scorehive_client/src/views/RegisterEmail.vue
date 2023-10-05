<template>
  <section class="position-relative background-radial-gradient overflow-hidden">
    <div class="position-absolute top-0 start-0 ms-14 mt-6 text-white fw-bold">
      <Router-link :to="{ name: 'SignIn' }">
        <img style="width: 200px" :src="scorehive" alt="Scorehive logo" />
      </Router-link>
    </div>
    <div class="min-vh-100 d-flex align-items-center">
      <div
        class="container px-4 py-5 px-md-5 text-center text-lg-start my-5 min-vh-100"
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
            <div class="card bg-glass">
              <div class="card-body px-4 py-5 px-md-5">
                <form>
                  <div class="row">
                    <div class="col-md-12 mb-4 text-center">
                      <h4>Register Your Email</h4>
                    </div>
                  </div>
                  <div class="col-md-12">
                    <!-- Email input -->
                    <div class="form-floating">
                      <input
                        type="email"
                        class="form-control"
                        id="floatingEmail"
                        placeholder="name@example.com"
                        v-model="email"
                      />
                      <label class="form-label text-muted" for="floatingEmail"
                        >Email address</label
                      >
                      <div
                        v-for="error of v$.email.$errors"
                        :key="error"
                        class="error"
                      >
                        <span
                          v-if="error.$params.type == 'required'"
                          class="text-danger"
                          >Please enter your email</span
                        >
                        <span
                          v-if="error.$params.type == 'email'"
                          class="text-danger"
                          >Please enter a valid email</span
                        >
                      </div>
                    </div>
                    <div v-if="v$.email.$errors.length == 0" class="mb-4"></div>
                  </div>
                  <!-- Submit button -->
                  <ButtonComponent
                    class="mb-4 py-3"
                    fullWidth
                    variant="gradient"
                    color="primary"
                    :disabled="isLoading"
                    @click.prevent="submit()"
                    id="registerEmail"
                    ><span
                      v-if="isLoading"
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                      aria-hidden="true"
                    ></span>
                    <span v-else class="fw-bold">Register</span></ButtonComponent
                  >
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <P
      class="position-absolute bottom-0 start-50 translate-middle-x fs-7 text-white"
    >
      © 2023 ScoreHive
    </P>
  </section>
</template>
<script>
import scorehive from "@/assets/img/logo_6.png";
import Swal from "sweetalert2";
import { sendEmail } from "@/services/authService";
import { useVuelidate } from "@vuelidate/core";
import errorCodes from "@/services/errorCodes.json";
import { required, email, maxLength } from "@vuelidate/validators";
import ButtonComponent from "@/components/Button.vue";
export default {
  components: {
    ButtonComponent,
  },
  setup() {
    return { v$: useVuelidate() };
  },
  data() {
    return {
      email: "",
      scorehive: scorehive,
      isLoading: false,
    };
  },
  validations() {
    return {
      email: {
        required,
        email,
        maxLength: maxLength(100),
      },
    };
  },
  methods: {
    async submit() {
      const isValid = await this.v$.$validate();
      if (isValid) {
        this.isLoading = true;
        let param = {
          email: this.email,
        };
        sendEmail(param).then(
          () => {
            Swal.fire({
              icon: "success",
              title: "",
              text: "Please check your email for the registration link",
            });
            this.$router.push({
              name: "SignIn",
            });
          },
          (error) => {
            this.isLoading = false;
            const errorMessage =
              errorCodes[error.response.data.error_code] ||
              "Oops.. Some unknown error occurred..!";
            this.$data.email = "";
            this.v$.$reset();
            Swal.fire({
              icon: "error",
              title: "Failed",
              text: errorMessage,
            });
            this.isLoading = false;
            this.$router.push({
              name: "register-email",
            });
          }
        );
      } else {
        this.isLoading = false;
      }
    },
  },
};
</script>
