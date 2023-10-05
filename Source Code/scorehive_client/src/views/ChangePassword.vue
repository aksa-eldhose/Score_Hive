<template>
  <NavBar />
  <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"
  />
  <section class="vh-100">
    <div class="container py-5 h-100">
      <div class="row d-flex align-items-center justify-content-center h-100">
        <div class="col-md-8 col-lg-7 col-xl-6">
          <img :src="imgpassword" class="img-fluid" alt="Phone image" />
        </div>
        <div class="col-md-7 col-lg-5 col-xl-5 offset-xl-1">
          <div class="form-box">
            <form @submit.prevent="submitForm" ref="myForm">
              <br />
              <h3 class="text-start">{{ $t("Change_password") }}</h3>
              <hr />

              <div class="mb-4">
                <label for="current-password" class="form-label">{{
                  $t("Current Password")
                }}</label>
                <div class="input-group">
                  <input
                    class="form-control"
                    id="current-password"
                    placeholder="Enter your password"
                    :type="showPassword.current ? 'text' : 'password'"
                    v-model="oldpassword"
                  />
                  <button
                    type="button"
                    @click="toggleShowPassword('current')"
                    class="btn btn-outline-secondary"
                    style="background-color: white; color: gray"
                  >
                    <i
                      :class="
                        showPassword.current ? 'far fa-eye' : 'fas fa-eye-slash'
                      "
                    ></i>
                  </button>
                </div>
                <span
                  v-for="(error, index) in v$.oldpassword.$errors"
                  :key="index"
                  class="text-danger fs-7"
                >
                  <small>{{ error.$message }}</small>
                </span>
              </div>
              <div class="mb-4">
                <label for="new-password" class="form-label">{{
                  $t("New Password")
                }}</label>
                <div class="input-group">
                  <input
                    class="form-control"
                    id="new-password"
                    v-model="password"
                    placeholder="Enter your new password"
                    :type="showPassword.new ? 'text' : 'password'"
                  />
                  <button
                    type="button"
                    @click="toggleShowPassword('new')"
                    class="btn btn-outline-secondary"
                    style="background-color: white; color: gray"
                  >
                    <i
                      :class="
                        showPassword.new ? 'far fa-eye' : 'fas fa-eye-slash'
                      "
                    ></i>
                  </button>
                </div>
                <span
                  v-if="v$.password.$errors.length > 0"
                  class="text-danger fs-7"
                >
                  <small>{{ $t("Please_enter_a_strong_password") }}</small>
                  <button class="btn btn-link btn-sm pt-0 btn-tooltip">
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
              <div class="mb-4">
                <label for="confirm-password" class="form-label">{{
                  $t("Confirm Password")
                }}</label>
                <div class="input-group">
                  <input
                    type="password"
                    class="form-control"
                    id="confirm-password"
                    v-model="confirmPassword"
                    placeholder="Re-enter your new password"
                  />
                </div>
                <span
                  v-for="(error, index) in v$?.confirmPassword?.$errors"
                  :key="index"
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
                  <small>{{ $t("Passwords do not match") }}</small>
                </div>
              </div>
              <div class="text-center">
                <cbutton
                  class="btn btn-primary"
                  type="button"
                  color="primary"
                  :disabled="v$.$error || !passwordsMatch"
                  @click="submit()"
                  style="margin-right: 10px"
                >
                  <span
                    v-if="isLoading"
                    class="spinner-border spinner-border-sm me-2"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  <span v-else
                    ><span>{{ $t("Change_Password") }}</span></span
                  ></cbutton
                >
              </div>
              <br />
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// Import necessary components and libraries
import imgpassword from "@/assets/img/imgpassword.avif";
import NavBar from "./NavBar.vue";
import { ChangePassword, checkCurrentPassword } from "@/services/authService";
import errorCodes from "@/services/errorCodes.json";
import { useVuelidate } from "@vuelidate/core";
import cbutton from "@/components/Button.vue";
import { required, minLength, maxLength, helpers } from "@vuelidate/validators";
import Swal from "sweetalert2";
export default {
  components: {
    NavBar,
    cbutton,
  },
  setup() {
    return { v$: useVuelidate() };
  },
  data() {
    return {
      oldpassword: "",
      password: "",
      confirmPassword: "",
      error: null,
      errorMessage: null,
      success: false,
      showPassword: {
        current: false,
        new: false,
        confirm: false,
      },
      imgpassword,
    };
  },
  computed: {
    passwordsMatch() {
      return this.password === this.confirmPassword;
    },
  },
  validations() {
    return {
      oldpassword: {
        req: helpers.withMessage(
          "Current password required",
          (value) => value != ""
        ),
      },
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
          "Confirm password required",
          (value) => value != ""
        ),
      },
    };
  },
  methods: {
    toggleShowPassword(field) {
      this.showPassword[field] = !this.showPassword[field];
    },
    resetFormAndRedirect() {
      this.oldpassword = "";
      this.confirmPassword = "";
      this.password = "";
      this.$router.push({
        name: "ChangePassword",
      });
    },
    async submit() {
      const isValid = await this.v$.$validate();
      if (!isValid || !this.passwordsMatch) {
        return;
      }
      try {
        await this.checkCurrentPassword();
        const confirmed = await this.showChangePasswordConfirmationDialog();
        if (confirmed) {
          await this.changePassword();
        } else {
          this.resetFormAndRedirect();
        }
      } catch (error) {
        const errorMessage =
          errorCodes[error.response?.data?.error_code] ||
          "Some unknown error occurred..!";
        Swal.fire({ icon: "error", title: "Oops...", text: errorMessage });
        this.resetFormAndRedirect();
      }
    },
    async checkCurrentPassword() {
      const params = { current_password: this.oldpassword };
      await checkCurrentPassword(params);
    },
    async showChangePasswordConfirmationDialog() {
      const confirmed = await Swal.fire({
        icon: "question",
        title: "Are you sure you want to change your password?",
        text: "Changing your password will log you out of your account.",
        showCancelButton: true,
        confirmButtonText: "Yes",
        cancelButtonText: "No",
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
      });
      return confirmed.value;
    },
    async changePassword() {
      const param = {
        current_password: this.oldpassword,
        new_password: this.password,
        confirm_password: this.confirmPassword,
      };
      if (
        this.password === this.confirmPassword &&
        this.password !== this.oldpassword
      ) {
        await ChangePassword(param);
        Swal.fire({
          icon: "success",
          title: "Your password has been changed successfully!!!",
          html: "Logging Out...",
          timer: 3000,
          timerProgressBar: true,
          didOpen: () => {
            Swal.showLoading();
          },
          willClose: () => {
            localStorage.clear();
            this.$router.push({ name: "SignIn" });
          },
        });
      } else {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Current password and new password cannot be the same.",
        });
        this.resetFormAndRedirect();
      }
    },
  },
};
</script>
<style scoped>
.form-box {
  max-width: 500px;
  margin: auto;
  margin-left: 20px;
  padding: 50px;
  background: #ffffff;
  box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
}
#current-password::placeholder,
#new-password::placeholder,
#confirm-password::placeholder {
  font-size: 14px;
}
#formContent {
  border-radius: 10px 10px 10px 10px;
  background: #fff;
  padding: 20px;
  width: 90%;
  max-width: 450px;
  position: relative;
  box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
}

.btn-tooltip {
  position: absolute;
  display: inline-block;
}

.btn-tooltip .tooltip {
  position: absolute;
  top: 100%;
  left: 30%;
  transform: translateX(-50%);
  background-color: rgba(248, 215, 215, 0.993);
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
  top: -10px;
  left: 30%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: transparent transparent #f00 transparent;
}

@media screen and (min-width: 642px) and (max-width: 800px) {
  .formContent {
    width: 100%;
  }
}
</style>
