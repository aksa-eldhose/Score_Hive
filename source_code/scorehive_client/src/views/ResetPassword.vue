<template>
  <section class="position-relative background-radial-gradient overflow-hidden">
    <div class="position-absolute top-0 start-0 ms-14 mt-6 text-white fw-bold">
      <RouterLink
        :to="{ name: 'SignIn' }"
        class="text-sm ml-2 mr-2 hover:text-blue-500 cursor-pointer"
      >
        <img style="width: 200px" :src="scorehive" alt="Image" />
      </RouterLink>
    </div>
    <div class="min-vh-100 d-flex align-items-center">
      <div class="container px-4 py-5 px-md-5 text-center text-lg-start my-5">
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
              A complete solution to manage your tournaments and matches
            </p>
          </div>

          <div class="col-lg-6 mb-5 mb-lg-0 position-relative">
            <div class="p-5 mx-10 card bg-glass shadow-lg">
              <div class="card-body px-4 py-5 px-md-5">
                <form @submit.prevent="submitForm" ref="myForm">
                  <div class="row">
                    <div class="col-md-12 mb-4">
                      <h4>Reset Your Password</h4>
                      <h6></h6>
                    </div>
                  </div>
                  <!-- Password input -->
                  <div class="form-group mb-4">
                    <label>New Password</label>
                    <input
                      type="password"
                      class="form-control"
                      id="password"
                      v-model="password"
                      placeholder="Enter your new Password"
                    />
                    <span
                      v-if="v$.password.$errors.length > 0"
                      class="text-danger fs-7"
                    >
                      <small>Please enter a strong password</small>
                      <button class="btn btn-link btn-sm p-0 ml-2 btn-tooltip">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          fill="currentColor"
                          class="bi bi-info-circle-fill"
                          viewBox="0 0 16 16"
                        >
                          <path
                            d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"
                          />
                        </svg>
                        <div class="tooltip">
                          {{ $t("tooltip") }}
                        </div>
                      </button>
                    </span>
                  </div>
                  <div class="form-group mb-4">
                    <label for="confirm-password">Confirm Password</label>
                    <input
                      type="password"
                      class="form-control"
                      id="confirm-password"
                      v-model="confirmPassword"
                      placeholder="Re-enter your password"
                    />

                    <span
                      v-for="(error, index) in v$?.confirmPassword?.$errors" :key="index"
                      class="text-danger fs-7"
                    >
                      <small>{{ error.$message }}</small>
                      <div
                        v-if="index !== v$?.confirmPassword?.$errors.length - 1"
                      ></div>
                    </span>
                    <div
                      v-if="password && confirmPassword && !passwordsMatch"
                      class="text-danger fs-7"
                    >
                      <small>Passwords do not match</small>
                    </div>
                  </div>
                  <div class="text-center">
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
                      <span v-else class="fw-bold">
                        Reset Password</span
                      ></cbutton
                    >
                  </div>
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

<style scoped>
.btn-tooltip {
  position: relative;
  display: inline-block;
}

.btn-tooltip .tooltip {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(248, 247, 247, 0.993);
  color: #eb2a2a;
  padding: 10px;
  border-radius: 5px;
  margin-top: 5px;
  white-space: pre-line;
  visibility: hidden;
  opacity: 0;
  transition: opacity 0.3s;
  width: 200px;
}

.btn-tooltip:hover .tooltip {
  visibility: visible;
  opacity: 1;
}

.btn-tooltip .tooltip::before {
  content: "";
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: transparent transparent #f00 transparent;
}
</style>
<script>
// Import necessary components and libraries
import cric from "@/assets/img/cric.png";
import scorehive from "@/assets/img/logo_6.png";
import { Forgotpassword } from "@/services/authService";
import { useVuelidate } from "@vuelidate/core";
import errorCodes from "@/services/errorCodes.json";
import router from "@/router";
import { required, minLength, maxLength, helpers } from "@vuelidate/validators";
import Swal from "sweetalert2";
import cbutton from "@/components/Button.vue";
export default {
  components: {
    cbutton,
  },
  // Define the setup function to initialize v$ object for validations
  setup() {
    return { v$: useVuelidate() };
  },
  beforeRouteLeave(to, from, next) {
    if (to.name === "verify_ResetPassword") {
      // Prevent the navigation to the email verification page
      next(false);
    } else {
      // Allow the navigation to proceed
      next();
    }
  },
  // Set data
  data() {
    return {
      password: "",
      email: "",
      confirmPassword: "",
      error: null,
      success: false,
      cric: cric,
      scorehive: scorehive,
    };
  },
  computed: {
    passwordsMatch() {
      return this.password === this.confirmPassword;
    },
  },
  // Define validation rules
  validations() {
    return {
      password: {
        required,
        maxLength: maxLength(20),
        minLength: minLength(8),
        containsUppercase: function (value) {
          return /[A-Z]/.test(value);
        },
        containsLowercase: function (value) {
          return /[a-z]/.test(value);
        },
        containsNumber: function (value) {
          return /\d/.test(value);
        },
        containsSpecial: function (value) {
          return /[#?!@$%^&*-]/.test(value);
        },
        noSpaces: function (value) {
          return !/\s/.test(value);
        },
      },
      confirmPassword: {
        req: helpers.withMessage(
          "Confirm Password required",
          (value) => value != ""
        ),
      },
    };
  },
  methods: {
    async submit() {
      const isValid = await this.v$.$validate();
      if (isValid) {
        let param = {
          email: localStorage.getItem("email"),
          password: this.password,
          confirm_password: this.confirmPassword,
        };
        if (this.password == this.confirmPassword) {
          Forgotpassword(param).then(
            (response) => {
              Swal.fire({
                position: "center",
                icon: "success",
                title: response.data.message,
                showConfirmButton: false,
                timer: 1500,
              });
              this.$refs.myForm.reset();
              this.$router.push({
                name: "SignIn",
              });
              localStorage.clear();
            },
            (error) => {
              const errorMessage =
                errorCodes[error.response.data.error_code] ||
                "Oops.. Some unknown error occurred..!";

              Swal.fire({
                icon: "error",
                title: "Password Reset Failed",
                text: errorMessage,
              });
              router.push("/SendEmailResetPassword");
            }
          );
        }
      }
    },
  },
};
</script>
