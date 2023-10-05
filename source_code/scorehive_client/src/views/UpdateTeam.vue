<template>
  <NavBar />
  <section class="vh-100">
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-6 px-0 d-none d-sm-block">
          <img
            :src="cricplrs"
            alt="Create Team"
            class="w-100 vh-100"
            style="object-fit: scale-down; object-position: left"
          />
        </div>
        <div class="col-sm-6 text-black">
          <div class="px-5 ms-xl-4"></div>
          <div
            class="d-flex align-items-center h-custom-2 px-5 ms-xl-4 mt-5 pt-5 pt-xl-0 mt-xl-n5"
          >
            <form style="width: 23rem" @submit.prevent="submit">
              <h3
                class="fw-normal text-center mb-3 pb-3"
                style="letter-spacing: 1px"
              >
                Update team details
              </h3>
              <div class="form-outline mb-4">
                <div class="d-flex justify-content-center position-relative">
                  <LogoContainer
                    :showImage="showDelete && logo !== 1"
                    :imageUrl="imageUrl"
                    :emptyImageContent="emptyImageContent"
                    containerWidth="150px"
                    containerHeight="150px"
                    borderRadius="50%"
                  />
                  <label
                    v-if="showDelete"
                    for="delete"
                    class="delete-icon p-1 d-flex justify-content-center text-danger bg-glass position-absolute bottom-0"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 24 24"
                      fill="currentColor"
                      class="w-6 h-6"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M16.5 4.478v.227a48.816 48.816 0 013.878.512.75.75 0 11-.256 1.478l-.209-.035-1.005 13.07a3 3 0 01-2.991 2.77H8.084a3 3 0 01-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 01-.256-1.478A48.567 48.567 0 017.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 013.369 0c1.603.051 2.815 1.387 2.815 2.951zm-6.136-1.452a51.196 51.196 0 013.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 00-6 0v-.113c0-.794.609-1.428 1.364-1.452zm-.355 5.945a.75.75 0 10-1.5.058l.347 9a.75.75 0 101.499-.058l-.346-9zm5.48.058a.75.75 0 10-1.498-.058l-.347 9a.75.75 0 001.5.058l.345-9z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    <button
                      type="button"
                      id="delete"
                      @click="removeLogo"
                      style="display: none"
                    ></button>
                  </label>
                  <label
                    v-else
                    for="logo"
                    class="edit-icon p-1 d-flex justify-content-center position-absolute bottom-0"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke-width="1.5"
                      stroke="currentColor"
                      class="w-6 h-6"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
                      />
                    </svg>
                    <input
                      type="file"
                      id="logo"
                      ref="fileInput"
                      @change="onFileChange"
                      style="display: none"
                    />
                  </label>
                </div>
                <span v-if="msg" class="text-danger"
                  ><small>{{ msg }}</small></span
                >
              </div>
              <div class="form-outline mb-4">
                <label for="teamName" class="form-label">Team Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="teamName"
                  placeholder="Enter team name"
                  v-model.trim="teamName"
                />
                <div
                  v-for="(error, index) of v$.teamName.$errors" :key="index"
                  class="text-danger"
                >
                  <span v-if="index === 0 && error.$params.type == 'required'"
                    ><small>Please enter team name.</small></span
                  >
                  <span v-if="index === 0 && error.$params.type == 'maxLength'"
                    ><small>Team name is too long..!</small></span
                  >
                  <span v-if="index === 0 && error.$params.type == 'minLength'"
                    ><small>Team name is too short..!</small></span
                  >
                  <span
                    v-if="
                      index === 0 && error.$params.type === 'emojiNotAllowed'
                    "
                  >
                    <small>Emojis are not allowed.</small>
                  </span>
                </div>
              </div>
              <div class="form-outline mb-4">
                <label for="city" class="form-label">City</label>
                <select class="form-select" id="city" v-model.trim="city">
                  <option value="">Select City</option>
                  <option
                    v-for="city in cities"
                    :key="city.id"
                    :value="city.id"
                  >
                    {{ city.name }}
                  </option>
                </select>
                <div v-for="error of v$.city.$errors" :key="error" class="text-danger">
                  <span v-if="error.$params.type == 'required'"
                    ><small>Please select your city.</small></span
                  >
                  <span v-if="error.$params.type == 'maxLength'"
                    ><small>City name is too long..!</small></span
                  >
                </div>
              </div>
              <div class="d-flex pt-1 mb-4">
                <ButtonComponent
                  class="mb-4"
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
                  <span v-else>Submit</span></ButtonComponent
                >
                <ButtonComponent
                  class="mb-4 ms-2"
                  fullWidth
                  variant="outline"
                  color="primary"
                  @click.prevent="reset"
                  >Cancel</ButtonComponent
                >
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
<style scoped>
.edit-icon {
  width: 25px;
  height: 25px;
  background-color: #274e96;
  color: white;
  border-radius: 50%;
}

.delete-icon {
  width: 25px;
  height: 25px;
  border-radius: 50%;
}
</style>
<script>
import NavBar from "./NavBar.vue";
import cricplrs from "@/assets/img/cric-2plrs.jpg";
import logoImg from "@/assets/img/logos/tst-logo.jpg";
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength, minLength,helpers } from "@vuelidate/validators";
const { withParams } = helpers;
import Swal from "sweetalert2";
import errorCodes from "@/services/errorCodes.json";
import { updateTeam, getCity, getTeamDetail } from "@/services/teamService";
import ButtonComponent from "@/components/Button.vue";
import LogoContainer from "@/components/LogoContainer.vue";

const emojiNotAllowed = withParams({ type: "emojiNotAllowed" }, (value) => {
  const emojiRegex =
    /[\uD800-\uDBFF][\uDC00-\uDFFF]|\u200D|\uFE0F|[\u20D0-\u20FF]|[\u2700-\u27BF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|\uD83E[\uDC00-\uDFFF]/g;
  return !emojiRegex.test(value);
});
export default {
  components: {
    NavBar,
    ButtonComponent,
    LogoContainer,
  },
  setup() {
    return { v$: useVuelidate() };
  },
  name: "UpdateTeam",
  data() {
    return {
      teamName: "",
      city: "",
      logo: null,
      imageUrl: "",
      msg: "",
      isVisible: "",
      test: true,
      testUrl: logoImg,
      isLoading: false,
      cricplrs: cricplrs,
      teamId: 1,
      showDelete: false,
      cities: [],
      emptyImageContent: "LOGO",
    };
  },
  validations() {
    return {
      teamName: {
        required,
        maxLength: maxLength(30),
        minLength: minLength(2),
        emojiNotAllowed,
      },
      city: {
        required,
        maxLength: maxLength(30),
      },
    };
  },
  mounted() {
    this.fetchCities();
    this.getDetail();
  },
  methods: {
    getDetail() {
      let id = this.$route.query.teamId;
      getTeamDetail(id).then(
        (result) => {
          this.teamName = result.data.name;
          try {
            if (result.data.logo_url) {
              this.showDelete = true;
              this.imageUrl = require(`${process.env.VUE_APP_FILE_PATH}${result.data.logo_url}`);
            }
          } catch (error) {
            this.imageUrl = `${process.env.VUE_APP_FILE_PATH}${result.data.logo_url}`;
          }
          this.city = result.data.city.id;
          this.teamId = result.data.id;
        },
        () => {
          this.$router.push("not-found");
        }
      );
    },
    async submit() {
  const isValid = await this.v$.$validate();

  if (!isValid) {
    if (this.v$.description.$errors.length === 0) {
      window.scrollTo(0, 0);
    }
    return;
  }

  this.isLoading = true;

  const conditionsMap = {
    showDelete: "Do you want to continue without logo?",
    msg: "Your logo will not be changed because you selected an invalid file..!",
    logo: 1,
  };

  const message = Object.keys(conditionsMap)
    .find(condition => conditionsMap[condition]) || "To update team details";

  const result = await this.showConfirmationDialog(message);

  if (result.isConfirmed) {
    const formData = new FormData();
    formData.append("name", this.$data.teamName);
    formData.append("city", this.$data.city);
    if (this.$data.logo) {
      formData.append("logo_url", this.$data.logo);
    }

    updateTeam(formData, this.teamId).then(
      () => {
        this.$toast.show("Team Updated", { type: "success" });
        this.reset();
        this.$router.push({ name: "team-list" });
      },
      (err) => {
        this.isLoading = false;
        const errorMessage = errorCodes[err.response.data.error_code] || "Oops.. Some unknown error occurred..!";
        Swal.fire({ icon: "error", title: "Failed", text: errorMessage });
      }
    );
  } else {
    this.isLoading = false;
  }
},

async showConfirmationDialog(message) {
  return Swal.fire({
    title: "Are you sure?",
    text: message,
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Continue",
    cancelButtonText: "Cancel",
  });
},

    reset() {
      this.$router.push("/team-list");
    },
    onFileChange(event) {
      if (event.target.files.length > 0) {
        this.logo = event.target.files[0];
        this.validateFile(event.target.files[0]);
        this.createImageUrl();
        this.test = false;
      } else {
        // No file selected, retain the previous file name if available
        if (!this.logo) {
          event.target.value = "";
        }
      }
    },
    createImageUrl() {
      if (this.logo && this.logo != 1) {
        this.showDelete = true;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageUrl = e.target.result;
        };
        reader.readAsDataURL(this.logo);
      }
    },
    openFileSelector() {
      this.$refs.fileInput.click();
    },
    validateFile(logo) {
      const MAX_SIZE = 2048 * 1024; // 2mb
      const ALLOWED_TYPES = ["image/png", "image/jpg", "image/jpeg"];
      if (!ALLOWED_TYPES.includes(logo.type)) {
        this.msg = "Please select a valid image file (PNG, JPG, JPEG).";
        this.logo = ""; // clear the input
        return false;
      }
      if (logo.size > MAX_SIZE) {
        this.msg = "File size should be less than 2 MB.";
        this.logo = "";
        return false;
      }
      const img = new Image();
      this.logo = null;
      img.src = URL.createObjectURL(logo);
      img.onload = () => {
        this.msg = "";
        this.logo = logo;
        this.createImageUrl();
        return true;
      };
    },
    removeLogo() {
      this.logo = "1";
      (this.imageUrl = "");
      (this.showDelete = false);
    },
    fetchCities() {
      getCity().then((res) => {
        this.cities = res.data;
      });
    },
  },
};
</script>
