<template>
  <NavBar />
  <div>
    <div class="form-wrap">
      <h3 class="text-start" style="letter-spacing: 1px">
        Add a new tournament
      </h3>
      <hr />
      <form id="form" @submit.prevent="submit">
        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label id="name-label" for="Tournament"
                >{{ $t("Tournament_Name")
                }}<span class="required">*</span></label
              >
              <input
                type="text"
                name="name"
                id="name"
                placeholder="Enter your tournament name"
                class="form-control"
                v-model.trim="tournament_name"
              />
              <span
                v-for="(error, index) in v$?.tournament_name?.$errors"
                :key="index"
                class="text-danger fs-7"
              >
                <small>{{ error.$message }}</small>
              </span>
            </div>
          </div>

          <div class="col-md-6">
            <div class="form-group">
              <label id="name-label" for="City"
                >{{ $t("City") }}<span class="required">*</span></label
              >
              <input
                type="text"
                name="name"
                id="name"
                placeholder="Enter your city "
                class="form-control"
                v-model.trim="city"
              />
              <span
                v-for="(error, index) in v$?.city?.$errors"
                :key="index"
                class="text-danger fs-7"
              >
                <small>{{ error.$message }}</small>
              </span>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label>{{ $t("Ground") }}<span class="required">*</span></label>
              <input
                type="text"
                name="name"
                id="name"
                placeholder="Enter your ground name"
                class="form-control"
                v-model.trim="ground"
              />
              <span
                v-for="(error, index) in v$?.ground?.$errors"
                :key="index"
                class="text-danger fs-7"
              >
                <small>{{ error.$message }}</small>
              </span>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label
                >{{ $t("Start_Date") }}<span class="required">*</span></label
              >
              <input
                type="date"
                id="startdate"
                name="startdate"
                class="form-control"
                :min="minDate"
                placeholder="mm-dd-yyyy"
                v-model="startDate"
                @keydown="preventInput"
              />

              <span
                v-for="(error, index) in v$?.startDate?.$errors"
                :key="index"
                class="text-danger fs-7"
              >
                <small>{{ error.$message }}</small>
              </span>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label id="enddate" for="enddate"
                >{{ $t("End_Date") }}<span class="required">*</span></label
              >
              <input
                type="date"
                id="enddate"
                name="enddate"
                :min="minDate"
                class="form-control"
                placeholder="mm-dd-yyyy"
                v-model="enddate"
                @keydown="preventInput"
              />

              <span
                v-for="(error, index) in v$?.enddate?.$errors"
                :key="index"
                class="text-danger fs-7"
              >
                <small>{{ error.$message }}</small>
              </span>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-4">
            <div class="form-group">
              <label
                >{{ $t("Tournament_Category")
                }}<span class="required">*</span></label
              >
              <div class="custom-control custom-radio custom-control-inline">
                <input
                  type="radio"
                  id="customRadioInline1"
                  value="0"
                  name="customRadioInline1"
                  class="custom-control-input"
                  v-model="category"
                />&nbsp;
                <label class="custom-control-label" for="customRadioInline1">{{
                  $t("Open")
                }}</label>
              </div>
              <div class="custom-control custom-radio custom-control-inline">
                <input
                  type="radio"
                  id="customRadioInline2"
                  value="1"
                  name="customRadioInline1"
                  class="custom-control-input"
                  v-model="category"
                />&nbsp;
                <label class="custom-control-label" for="customRadioInline2">{{
                  $t("Corporate")
                }}</label>
              </div>
              <div class="custom-control custom-radio custom-control-inline">
                <input
                  type="radio"
                  id="customRadioInline3"
                  value="2"
                  name="customRadioInline1"
                  class="custom-control-input"
                  v-model="category"
                />&nbsp;
                <label class="custom-control-label" for="customRadioInline3">{{
                  $t("School")
                }}</label>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label
                >{{ $t("Ball_Type") }}<span class="required">*</span></label
              >
              <div class="custom-control custom-radio custom-control-inline">
                <input
                  type="radio"
                  id="Tennis"
                  value="0"
                  name="Tennis"
                  class="custom-control-input"
                  checked=""
                  v-model="ball_type"
                />&nbsp;
                <label class="custom-control-label" for="Tennis">{{
                  $t("Tennis")
                }}</label>
              </div>
              <div class="custom-control custom-radio custom-control-inline">
                <input
                  type="radio"
                  id="Leather"
                  value="1"
                  name="Leather"
                  class="custom-control-input"
                  v-model="ball_type"
                />&nbsp;
                <label class="custom-control-label" for="Leather">
                  {{ $t("Leather") }}</label
                >
              </div>
              <div class="custom-control custom-radio custom-control-inline">
                <input
                  type="radio"
                  id="Other"
                  value="2"
                  name="Other"
                  class="custom-control-input"
                  v-model="ball_type"
                />&nbsp;
                <label class="custom-control-label" for="Other">{{
                  $t("Other")
                }}</label>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label
                >{{ $t("Match_Type") }}<span class="required">*</span></label
              >
              <div class="custom-control custom-checkbox custom-control-inline">
                <input
                  type="radio"
                  class="custom-control-input"
                  name="yes"
                  value="0"
                  id="yes"
                  checked="true"
                  v-model="match_type"
                />&nbsp;
                <label class="custom-control-label" for="yes">{{
                  $t("Limited")
                }}</label>
              </div>
              <div class="custom-control custom-checkbox custom-control-inline">
                <input
                  type="radio"
                  class="custom-control-input"
                  name="no"
                  value="1"
                  id="no"
                  v-model="match_type"
                />&nbsp;
                <label class="custom-control-label" for="no">{{
                  $t("Test")
                }}</label>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12">
            <div class="form-group">
              <label>{{ $t("Description") }}</label>
              <textarea
                id="comments"
                class="form-control"
                name="comment"
                placeholder="Enter your comment here..."
                v-model="description"
              ></textarea>
              <div
                v-for="error of v$.description.$errors"
                :key="error"
                class="text-danger"
              >
                <span v-if="error.$params.type == 'maxLength'"
                  ><small>{{ $t("Description_maxLen") }}</small></span
                >
                <span v-if="error.$params.type == 'minLength'"
                  ><small>{{ $t("Description_minLen") }}</small></span
                >
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <div class="form-box">
              <div class="form-outline mb-4">
                <div class="d-flex justify-content-center position-relative">
                  <LogoContainer
                    :showImage="showDeletelogo && logo !== 1"
                    :imageUrl="imageUrl"
                    :emptyImageContent="emptyImageContent"
                    containerWidth="150px"
                    containerHeight="150px"
                    borderRadius="50%"
                  />
                  <label
                    v-if="showDeletelogo"
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
                    for="logos"
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
                      id="logos"
                      @change="onLogoChange"
                      style="display: none"
                    />
                  </label>
                </div>
                <div class="text-center">
                  <span v-if="msg2" class="text-danger"
                    ><small>{{ msg2 }}</small></span
                  >
                  <span v-else class="p-3"></span>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-box">
              <div class="form-outline mb-4">
                <div class="d-flex justify-content-center position-relative">
                  <BannerContainer
                    :showImage="showDelete && banner !== 1"
                    :bannerUrl="bannerUrl"
                    :emptyImageContent="emptyImageContent"
                    containerWidth="350px"
                    containerHeight="150px"
                    borderRadius="0%"
                  />
                  <label
                    v-if="showDelete"
                    for="deletebanner"
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
                    <cbutton
                      type="button"
                      id="deletebanner"
                      @click="removeBanner"
                      style="display: none"
                    ></cbutton>
                  </label>
                  <label
                    v-else
                    for="banner"
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
                      id="banner"
                      @change="onBannerChange"
                      style="display: none"
                    />
                  </label>
                </div>
                <div class="text-center">
                  <span v-if="msg" class="text-danger"
                    ><small>{{ msg }}</small></span
                  >
                  <span v-else class="p-3"></span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <br /><br />
        <div class="row">
          <div class="d-flex pt-1 mb-4">
            <cbutton
              class="btn btn-primary"
              type="button"
              color="primary"
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
                ><span>{{ $t("PUBLISH") }}</span></span
              ></cbutton
            >
            <cbutton
              type="button"
              color="white"
              class="btn btn-outline-primary"
              @click="routes()"
            >
              {{ $t("CANCEL") }}
            </cbutton>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import NavBar from "./NavBar.vue";
import { useVuelidate } from "@vuelidate/core";
import { getCity } from "@/services/teamService";
import { createTournament, getGround } from "@/services/tournamentService";
import { required, maxLength, minLength, helpers } from "@vuelidate/validators";
import { userProfile } from "@/services/authService";
import cric from "@/assets/img/cric.png";
import Swal from "sweetalert2";
import cbutton from "@/components/Button.vue";
import errorCodes from "@/services/errorCodes.json";
import LogoContainer from "@/components/LogoContainer.vue";
import BannerContainer from "@/components/BannerContainer.vue";
const regexPhone = helpers.regex(/^\+\d{1,3} \d{10}$/);

export default {
  components: {
    NavBar,
    cbutton,
    LogoContainer,
    BannerContainer,
  },
  setup() {
    return { v$: useVuelidate() };
  },
  mounted() {
    this.fetchCities();
    this.fetchGround();
    this.getDetail();
    const currentDate = new Date().toISOString().split("T")[0];
    this.minDate = currentDate;
  },
  data() {
    return {
      tournament_name: "",
      city: "",
      ground: "",
      grounds: [],
      organiser_name: "",
      contact: "",
      startDate: "",
      enddate: "",
      category: "0",
      ball_type: "0",
      match_type: "0",
      description: "",
      banner: null,
      logo: null,
      cities: [],
      minDate: "",
      cric: cric,
      msg: "",
      msg2: "",
      imageUrl: "",
      bannerUrl: "",
      showDeletelogo: false,
      showDelete: false,
      isLoading: false,
    };
  },
  validations() {
    return {
      tournament_name: {
        maxLength: helpers.withMessage(
          "Tournament name is too long..!",
          maxLength(100)
        ),
        minLength: helpers.withMessage(
          "Tournament name is too short..!",
          minLength(2)
        ),
        req: helpers.withMessage(
          "Please enter tournament name.",
          (value) => value != ""
        ),
      },
      city: {
        maxLength: helpers.withMessage(
          "City name is too long..!",
          maxLength(100)
        ),
        minLength: helpers.withMessage(
          "City name is too short..!",
          minLength(2)
        ),
        req: helpers.withMessage("Please enter city.", (value) => value != ""),
      },
      ground: {
        maxLength: helpers.withMessage(
          "Ground name is too long..!",
          maxLength(100)
        ),
        minLength: helpers.withMessage(
          "Ground name is too short..!",
          minLength(2)
        ),
        req: helpers.withMessage(
          "Please enter ground name.",
          (value) => value != ""
        ),
      },
      organiser_name: {
        maxLength: helpers.withMessage(
          "Organiser name is too long..!",
          maxLength(100)
        ),
        minLength: helpers.withMessage(
          "Organiser name is too short..!",
          minLength(2)
        ),
      },
      contact: {
        regexphone: helpers.withMessage(
          "Phone number should be in +999 9999999999 format",
          regexPhone
        ),
      },
      startDate: {
        req: helpers.withMessage(
          "Please select start date.",
          (value) => value != ""
        ),
      },
      enddate: {
        req: helpers.withMessage(
          "Please select end date.",
          (value) => value != ""
        ),
        dateSameOrAfterStartDate: helpers.withMessage(
          "End date should be same or after the startdate",
          (value, vm) => {
            return value ? value >= vm.startDate : true;
          }
        ),
      },
      category: {
        required,
      },
      ball_type: {
        required,
      },
      match_type: {
        required,
      },
      description: {
        maxLength: maxLength(500),
        minLength: minLength(1),
      },
    };
  },
  methods: {
    async submit() {
      const isValid = await this.v$.$validate();
      if (!isValid) {
        if (this.v$.description.$errors.length === 0) {
          window.scrollTo(0, 0);
        }
        return;
      }

      this.isLoading = true;

      const hasLogo = !!this.logo;
      const hasBanner = !!this.banner;
      const confirmationText = this.getConfirmationText(hasLogo, hasBanner);
      const confirmed = await this.showConfirmationDialog(confirmationText);

      if (confirmed) {
        try {
          const formData = this.buildFormData();
          await createTournament(formData);
          this.handleSuccessResponse();
        } catch (err) {
          this.handleErrorResponse(err);
        }
      } else {
        this.isLoading = false;
      }
    },
    getConfirmationText(hasLogo, hasBanner) {
      if (!hasLogo && !hasBanner)
        return "Create tournament without a logo and banner?";
      if (!hasLogo && hasBanner) return "Create tournament without a logo?";
      if (hasLogo && !hasBanner) return "Create tournament without a banner?";
      return "You are about to create a tournament";
    },
    async showConfirmationDialog(confirmationText) {
      const result = await Swal.fire({
        title: "Are you sure?",
        text: confirmationText,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Ok",
        cancelButtonText: "Cancel!",
      });
      return result.isConfirmed;
    },
    buildFormData() {
      const formData = new FormData();
      const data = this.$data;
      formData.append("name", data.tournament_name);
      formData.append("city", data.city);
      formData.append("ground", data.ground);
      formData.append("start_date", data.startDate);
      formData.append("end_date", data.enddate);
      formData.append("match_type", data.match_type);
      formData.append("ball_type", data.ball_type);
      formData.append("tournament_type", data.category);

      if (this.description) {
        formData.append("description", data.description);
      }
      if (this.logo) {
        formData.append("logo_url", data.logo);
      }
      if (this.banner) {
        formData.append("banner_url", data.banner);
      }

      return formData;
    },
    handleSuccessResponse() {
      this.$toast.show("Tournament Created", {
        type: "success",
      });
      this.reset();
      this.$router.push({
        name: "tournament-list",
      });
    },
    handleErrorResponse(err) {
      this.isLoading = false;
      const errorMessage =
        errorCodes[err.response.data.error_code] ||
        "Oops.. Some unknown error occurred..!";
      Swal.fire({
        icon: "error",
        title: "Failed",
        text: errorMessage,
      });
    },

    currentDate() {
      const today = new Date().toISOString().split("T")[0];
      return today;
    },
    fetchGround() {
      getGround().then((res) => {
        this.grounds = res.data;
      });
    },
    fetchCities() {
      getCity().then((res) => {
        this.cities = res.data;
      });
    },
    reset() {
      this.tournament_name = "";
      this.city = "";
      this.ground = "";
      this.startDate = "";
      this.enddate = "";
      this.description = "";
      this.logo = null;
      this.banner = null;
      this.msg = "";
      this.msg2 = "";
      const input = document.getElementById("logos");
      if (input) {
        input.value = "";
      }
      const inputbanner = document.getElementById("banner");
      if (inputbanner) {
        inputbanner.value = "";
      }
      this.imageUrl = "";
      this.bannerUrl = "";
      this.showDeletelogo = false;
      this.showDelete = false;
    },

    preventInput(event) {
      event.preventDefault();
    },
    getDetail() {
      this.organiser_name = localStorage.getItem("User_name");
      this.contact = localStorage.getItem("Phone_number");
      userProfile().then(
        (res) => {
          this.organiser_name = res.data.Name;
          this.contact = res.data.Phone_Number;
          localStorage.setItem("User_name", res.data.Name);
          localStorage.setItem("Phone_number", res.data.Phone_Number);
        },
        (error) => {
          const errorMessage =
            errorCodes[error.response?.data?.error_code] ||
            "Some unknown error occurred..!";
          Swal.fire({ icon: "error", title: "Oops...", text: errorMessage });
        }
      );
    },
    routes() {
      this.$router.push({
        name: "tournament-list",
      });
    },
    validateFile(file) {
      const MAX_SIZE = 2048 * 1024; // 2mb
      const ALLOWED_TYPES = ["image/png", "image/jpg", "image/jpeg"];

      if (!ALLOWED_TYPES.includes(file.type)) {
        return "Please select a valid image file (PNG, JPG, JPEG).";
      }

      if (file.size > MAX_SIZE) {
        return "File size should be less than 2 MB.";
      }
      return "";
    },
    createImageUrl() {
      if (this.logo) {
        this.showDeletelogo = true;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageUrl = e.target.result;
        };
        reader.readAsDataURL(this.logo);
      }
    },
    createBannerUrl() {
      if (this.banner) {
        this.showDelete = true;
        const reader = new FileReader();
        reader.onload = (e) => {
          this.bannerUrl = e.target.result;
        };
        reader.readAsDataURL(this.banner);
      }
    },
    onLogoChange(event) {
      if (event.target.files.length > 0) {
        let validateResult = this.validateFile(event.target.files[0]);
        this.msg2 = validateResult;
        if (validateResult) {
          this.removeLogo();
          return;
        }
        this.logo = event.target.files[0];
        this.createImageUrl();
      } else {
        if (!this.logo) {
          event.target.value = "";
        }
      }
    },
    onBannerChange(event) {
      if (event.target.files.length > 0) {
        let validateResult = this.validateFile(event.target.files[0]);
        this.msg = validateResult;
        if (validateResult) {
          this.removeBanner();
          return;
        }
        this.banner = event.target.files[0];
        this.createBannerUrl();
      } else {
        if (!this.banner) {
          event.target.value = "";
        }
      }
    },
    removeLogo() {
      this.logo = null;
      this.imageUrl = "";
      const input = document.getElementById("logo");
      if (input) {
        input.value = "";
      }
      this.showDeletelogo = false;
    },
    removeBanner() {
      this.banner = null;
      this.bannerUrl = "";
      const input = document.getElementById("banner");
      if (input) {
        input.value = "";
      }
      this.showDelete = false;
    },
  },
};
</script>
<style scoped>
.container {
  max-width: 1230px;
  width: 100%;
}

h1 {
  font-weight: 700;
  font-size: 45px;
  font-family: "Roboto", sans-serif;
}
.form-wrap {
  background: rgb(255, 255, 255);
  width: 100%;
  max-width: 1100px;
  padding: 50px;
  margin-inline: auto;
  margin-bottom: 5%;
  margin-top: 3%;
  box-shadow: 0px 0px 40px rgba(0, 0, 0, 0.15);
}
.form-group {
  margin-bottom: 25px;
}

label {
  margin-bottom: 10px;
  font-size: 18px;
}

textarea.form-control {
  height: 160px;
  padding-top: 15px;
  resize: none;
}
.form-box {
  max-width: 1000px;
  margin: auto;
  font-size: 14px;
  margin-left: 10px;
  padding: 50px;
  padding-bottom: 15px;
  background: #ffffff;
  box-shadow: 0 10px 20px 0 rgba(0, 0, 0, 0.3);
}
.required {
  color: red;
}
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
