<template>
  <section class="background-radial-gradient overflow-hidden position-relative">
    <div class="position-absolute top-0 start-0 ms-14 mt-6 text-white fw-bold">
      <Router-link :to="{ name: 'SignIn' }">
        <img style="width: 200px" :src="scorehive" alt="Image" />
      </Router-link>
    </div>
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
            <span style="color: hsl(218, 81%, 75%)">to manage your games</span>
          </h1>
          <p class="mb-4 opacity-70" style="color: hsl(218, 81%, 85%)">
            A complete solution to manage your cricket tournaments and matches
          </p>
        </div>
        <div class="col-lg-6 mb-5 mb-lg-0 position-relative">
          <GlassCard>
            <div class="card-body px-4 py-5 px-md-5">
              <form>
                <div class="row">
                  <div class="col-md-12 mb-4 text-center">
                    <h2>Sign Up</h2>
                  </div>
                </div>
                <div class="row text-start">
                  <div class="col-md-12">
                    <!-- Name input -->
                    <div class="form-floating">
                      <input
                        type="text"
                        class="form-control"
                        id="floatingEmail"
                        placeholder="Name"
                        v-model.trim="name"
                      />
                      <label class="form-label text-muted" for="floatingEmail"
                        >Name</label
                      >
                      <span
                        v-if="v$.name.$errors.length > 0"
                        class="text-danger fs-7"
                      >
                        <small>Please enter a valid name</small>
                        <button
                          class="btn btn-link btn-sm p-0 ml-2 btn-tooltip"
                          @click="disableTooltip"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="16"
                            height="16"
                            fill="#eb2a2a"
                            class="bi bi-info-circle-fill"
                            viewBox="0 0 16 16"
                          >
                            <path
                              d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"
                            />
                          </svg>
                          <div class="tooltip">
                            Name must contain:<br />
                            Only alphabets and spaces<br />
                            Length of name should be between 2-100 characters<br />
                          </div>
                        </button>
                      </span>
                    </div>
                    <div v-if="v$.name.$errors.length == 0" class="pb-4"></div>
                  </div>
                </div>
                <!-- Phone input -->
                <div class="form-floating text-start">
                  <input
                    type="text"
                    class="form-control"
                    id="floatingPhone"
                    placeholder="Phone"
                    v-model.trim="phone"
                  />
                  <label class="form-label text-muted" for="floatingPhone"
                    >Phone</label
                  >
                  <span
                    v-for="error in v$.phone.$errors"
                    :key="error"
                    class="text-danger fs-7"
                  >
                    <small>{{ error.$message }} </small></span
                  >
                </div>
                <div v-if="v$.phone.$errors.length == 0" class="pb-4"></div>
                <!-- Password input -->
                <div class="form-floating text-start">
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
                <span
                  v-if="v$.password.$errors.length > 0"
                  class="text-danger fs-7"
                >
                  <small>Please enter a strong password</small>
                  <button
                    class="btn btn-link btn-sm p-0 ml-2 btn-tooltip"
                    @click="disableTooltip"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      fill="#eb2a2a"
                      class="bi bi-info-circle-fill"
                      viewBox="0 0 16 16"
                    >
                      <path
                        d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"
                      />
                    </svg>
                    <div class="tooltip">
                      Password must contain:<br />
                      At least 1 capital letter<br />
                      At least 1 small letter<br />
                      At least 1 special character<br />
                      At least 1 digit<br />
                      Length of password should be 8-20 characters<br />
                    </div>
                  </button>
                </span>
                <div v-if="v$.password.$errors.length == 0" class="pb-4"></div>
                <div class="form-floating text-start">
                  <input
                    type="password"
                    class="form-control"
                    id="floatingCPassword"
                    placeholder="Confirm Password"
                    v-model.trim="cpassword"
                  />
                  <label class="form-label text-muted" for="floatingCPassword"
                    >Confirm Password</label
                  >
                </div>
                <span
                  v-for="(error, index) in v$?.cpassword?.$errors"
                  :key="error"
                  class="text-danger fs-7"
                >
                  <small> {{ error.$message }}</small>
                  <div v-if="index !== v$?.cpassword?.$errors.length - 1"></div>
                </span>
                <div
                  v-if="password && cpassword && !passwordsMatch"
                  class="text-danger fs-7"
                >
                  <small>Passwords do not match</small>
                </div>
                <div v-if="v$.cpassword.$errors.length == 0" class="pb-4"></div>
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
                <ButtonComponent
                  class="mb-4 py-3"
                  fullWidth
                  variant="gradient"
                  color="primary"
                  :disabled="isLoading"
                  @click.prevent="submit()"
                  id="signUp"
                  ><span
                    v-if="isLoading"
                    class="spinner-border spinner-border-sm me-2"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  <span v-else class="fw-bold">Sign up</span></ButtonComponent
                >
              </form>
              <div class="d-flex justify-content-between">
                <p class="fs-7 fw-normal cursor-pointer">Already registered?</p>
                <RouterLink
                  :to="{ name: 'SignIn' }"
                  class="text-sm ml-2 mr-2 hover:text-blue-500 cursor-pointer"
                >
                  SignIn
                </RouterLink>
              </div>
            </div>
          </GlassCard>
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
import errorCodes from "@/services/errorCodes.json";
import { useVuelidate } from "@vuelidate/core";
import { register } from "@/services/authService";
import {
  required,
  minLength,
  maxLength,
  helpers,
} from "@vuelidate/validators";
import ButtonComponent from "@/components/Button.vue";
import GlassCard from "@/components/GlassCard.vue";
/*Regex for phone number validation*/
const regexPhone = helpers.regex(/^\+\d{1,3} \d{10}$/);
/**Regex for Name */
const regexName = helpers.regex(/^[a-zA-Z\s]+$/);
export default {
  name: "sign-up",
  components: {
    ButtonComponent,
    GlassCard,
  },
  mounted() {
    this.token = localStorage.getItem("Email_token");
  },
  setup() {
    return { v$: useVuelidate() };
  },

  data() {
    return {
      name: "",
      token: "",
      phone: "+91 ",
      password: "",
      cpassword: "",
      scorehive: scorehive,
      showPassword: false,
    };
  },
  computed: {
    passwordsMatch() {
      return this.password === this.cpassword;
    },
  },
  validations() {
    return {
      name: {
        required: helpers.withMessage("This field is required", required),
        regexName: helpers.withMessage(
          "Name should only contain alphabets and spaces",
          regexName
        ),
        maxLength: helpers.withMessage(
          "Name should be maximum 100 characters",
          maxLength(100)
        ),
        minLength: helpers.withMessage(
          "Name should be minimum 2 characters",
          minLength(2)
        ),
      },
      phone: {
        required: helpers.withMessage("This field is required", required),
        regexphone: helpers.withMessage(
          "Phone number should be in +999 9999999999 format",
          regexPhone
        ),
      },
      password: {
        required,
        maxLength: maxLength(20),
        minLength: minLength(8),
        containsUppercase: helpers.withMessage(
          "Password must contain at least one uppercase character",
          function (value) {
            const valid = /[A-Z]/.test(value);
            return valid;
          }
        ),
        containsLowercase: helpers.withMessage(
          "Password must contain at least one lowercase character",
          function (value) {
            return /[a-z]/.test(value);
          }
        ),
        containsNumber: helpers.withMessage(
          "Password must contain at least one number",
          function (value) {
            return /\d/.test(value);
          }
        ),
        containsSpecial: helpers.withMessage(
          "Password must contain at least one special character",
          function (value) {
            return /[#?!@$%^&*-]/.test(value);
          }
        ),
      },
      cpassword: {
        req: helpers.withMessage(
          "This field is required",
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
          name: this.name,
          token: this.token,
          phone_number: this.phone,
          password: this.password,
          confirm_password: this.cpassword,
        };
        if (this.password == this.cpassword) {
          register(param).then(
            (response) => {
              Swal.fire({
                icon: "success",
                text: response.data.message,
              });
              localStorage.removeItem("Email_token");
              this.$router.push({
                name: "SignIn",
              });
            },
            (error) => {
              if (
                error.response.data.error_code == 1008 &&
                error.response.data.message.phone_number
              ) {
                const errorMessage =
                  "A user already exists with this phone number";
                Swal.fire({
                  icon: "error",
                  title: "Failed",
                  text: errorMessage,
                });
              } else {
                const errorMessage =
                  errorCodes[error.response.data.error_code] ||
                  "Oops.. Some unknown error occurred..!";
                Swal.fire({
                  icon: "error",
                  title: "Failed",
                  text: errorMessage,
                });
              }
            }
          );
        }
      }
    },
    disableTooltip(event) {
      event.preventDefault(); // Prevent default click behavior
    },
  },
  beforeRouteLeave(to, from, next) {
    // Check if the user is leaving the sign-up page to go back to the email registration response page
    if (to.name === "register-email-response") {
      // Prevent the navigation to the email registration response page
      next(false);
    } else {
      // Allow the navigation to proceed
      next();
    }
  },
};
</script>
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
img {
  max-width: 100%;
  height: auto;
}
</style>
