<template>
  <NavBar />
  <div class="container mt-5">
    <div class="row d-flex justify-content-center align-items-center">
      <div class="col-md-5">
        <div class="card shadow">
          <div class="card-body px-5 py-5">
            <h4 id="heading" class="mb-4 text-center">Edit Profile</h4>
            <!-- Name input -->
            <div class="form-floating mb-4">
              <input
                type="text"
                class="form-control"
                id="floatingEmail"
                v-model.trim="name"
              />
              <label class="form-label text-muted" for="floatingEmail"
                >Name</label
              >
              <span class="text-danger" v-if="!validateName()"
                >Please enter name.</span
              >
              <span
                v-if="
                  validateName() &&
                  (!validateNameRegex() || !validateNameLength())
                "
                class="text-danger fs-7"
              >
                <button
                  class="btn btn-m p-0 ml-2 btn-tooltip d-flex"
                  style="color: #eb2a2a"
                  @click="disableTooltip"
                  id="nameToolTip"
                >
                  Please enter valid name&nbsp;
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
                    Length should be between 2-100<br />
                  </div>
                </button>
              </span>
            </div>
            <!-- Phone input -->
            <div class="form-floating mb-4">
              <input
                type="text"
                class="form-control"
                id="floatingEmail"
                v-model.trim="phone"
              />
              <label class="form-label text-muted" for="floatingEmail"
                >Phone Number</label
              >
              <span class="text-danger" v-if="!validatePhone()"
                >Please enter phone number</span
              >
              <span
                class="text-danger"
                v-if="validatePhone() && !validatePhoneRegex()"
                >Phone number should be in +999 9999999999 format</span
              >
            </div>
            <!-- Submit button -->
            <ButtonComponent
              class="mb-2"
              variant="gradient"
              color="primary"
              :disabled="myBoolean"
              @click.prevent="submit()"
              >Submit</ButtonComponent
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import NavBar from "./NavBar.vue";
import { userProfileEdit } from "@/services/authService";
import Swal from "sweetalert2";
import errorCodes from "@/services/errorCodes.json";
import ButtonComponent from "@/components/Button.vue";
export default {
  mounted() {
    this.name = localStorage.getItem("User_name");
    this.phone = localStorage.getItem("Phone_number");
  },
  components: {
    NavBar,
    ButtonComponent,
  },
  data() {
    return {
      name: "",
      phone: "+91 ",
      validForm: false,
    };
  },
  methods: {
    validateName() {
      return this.name.length > 0;
    },
    validateNameRegex() {
      /**Regex for Name */
      const regexName = /^[a-zA-Z\s]+$/;
      return regexName.test(this.name);
    },
    validateNameLength() {
      if (this.name.length >= 2 && this.name.length <= 100) return true;
    },
    validatePhone() {
      return this.phone.length > 0;
    },
    validatePhoneRegex() {
      /*Regex for phone number validation*/
      const regexPhone = /^\+\d{1,3} \d{10}$/;
      return regexPhone.test(this.phone);
    },
    async submit() {
      if (
        this.validateName() &&
        this.validateNameRegex() &&
        this.validateNameLength() &&
        this.validatePhone() &&
        this.validatePhoneRegex()
      ) {
        let param = {
          name: this.name,
          phone_number: this.phone,
        };
        userProfileEdit(param).then(
          () => {
            Swal.fire({
              icon: "success",
              text: "Profile updated successfully",
            });
            localStorage.removeItem("User_name");
            localStorage.removeItem("Phone_number");
            this.$router.push({
              name: "View-profile",
            });
          },
          (error) => {
            if (
              error.response.data.error_code == 1019 &&
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
      } else {
        this.validForm = true;
      }
    },
    disableTooltip(event) {
      event.preventDefault(); // Prevent default click behavior
    },
  },
};
</script>
<style scoped>
.card {
  margin-top: 20%;
  background-color: #ffffff;
  border-radius: 10px;
}
button {
  width: 100%;
}
.btn-tooltip .tooltip {
  display: inline-block;
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