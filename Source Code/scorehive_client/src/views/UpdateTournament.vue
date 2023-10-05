 <template>
  <NavBar />
  <div>
    <header class="header"></header>
    <div class="form-wrap">
      <h3 class="text-start" style="letter-spacing: 1px">
        {{ $t("Update_tournament") }}
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
                :title="FullTournamentName"
              />
              <span
                v-for="(error, index) in v$?.tournament_name?.$errors"
                :key="error"
                class="text-danger fs-7"
              >
                <small>{{ error.$message }}</small>
                <div
                  v-if="index !== v$?.tournament_name?.$errors.length - 1"
                ></div>
              </span>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group">
              <label>{{ $t("City") }}<span class="required">*</span></label>
              <input
                type="text"
                name="name"
                id="city"
                placeholder="Enter your city"
                class="form-control"
                v-model.trim="city"
                :title="FullCityName"
              />
              <div
                v-for="error of v$.city.$errors"
                :key="error"
                class="text-danger"
              >
                <span v-if="error.$params.type == 'required'"
                  ><small>{{ $t("Select_City_req") }}</small></span
                >
                <span v-if="error.$params.type == 'maxLength'"
                  ><small>{{ $t("Select_City_maxLen") }}</small></span
                >
                <span v-if="error.$params.type == 'minLength'"
                  ><small>{{ $t("Select_City_minLen") }}</small></span
                >
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label>{{ $t("Ground") }}<span class="required">*</span></label>
              <input
                type="text"
                name="name"
                id="ground"
                placeholder="Enter the ground name"
                class="form-control"
                v-model.trim="ground"
                :title="FullGroundName"
              />
              <div
                v-for="error of v$.ground.$errors"
                :key="error"
                class="text-danger"
              >
                <span v-if="error.$params.type == 'required'">
                  <small>{{ $t("Select_Ground_req") }}</small></span
                ><span v-if="error.$params.type == 'maxLength'"
                  ><small>{{ $t("Select_Ground_maxLen") }}</small></span
                >
                <span v-if="error.$params.type == 'minLength'"
                  ><small>{{ $t("Select_Ground_minLen") }}</small></span
                >
              </div>
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
                :disabled="isStart"
              />
              <span
                v-for="error in v$?.startDate?.$errors"
                :key="error"
                class="text-danger fs-7"
                id="startDateError"
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
                class="form-control"
                :min="minDate"
                placeholder="mm-dd-yyyy"
                v-model="enddate"
                @keydown="preventInput"
              />
              <span
                v-for="error in v$?.enddate?.$errors"
                :key="error"
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
                    <button
                      type="button"
                      id="deletebanner"
                      @click="removeBanner"
                      style="display: none"
                    ></button>
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
            <ButtonComponent
            class="btn btn-primary"
              type="button"
              color="primary"
              @click="submit()"
              style="margin-right: 10px"
            >
              <span>{{ $t("UPDATE") }}</span>
            </ButtonComponent>
            <ButtonComponent
            type="button"
              color="white"
              class="btn btn-outline-primary"
              @click="routes()"
            >
              {{ $t("CANCEL") }}
            </ButtonComponent>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import NavBar from "./NavBar.vue";
import ButtonComponent from "@/components/Button.vue";
import { useVuelidate } from "@vuelidate/core";
import { getCity } from "@/services/teamService";
import {
  getTournamentById,
  updateTournament,
  getGround,
} from "@/services/tournamentService";
import { required, maxLength, minLength, helpers } from "@vuelidate/validators";
import { userProfile } from "@/services/authService";
import cric from "@/assets/img/cric.png";
import Swal from "sweetalert2";
const regexPhone = helpers.regex(/^\+\d{1,3} \d{10}$/);
import LogoContainer from "@/components/LogoContainer.vue";
import BannerContainer from "@/components/BannerContainer.vue";
export default {
  components: {
    NavBar,
    LogoContainer,
    BannerContainer,
    ButtonComponent
  },
  setup() {
    return { v$: useVuelidate() };
  },
  mounted() {
    if (this.$route?.query?.tournamentId) {
      const secret = "tournament";
      try {
        this.tournamentId = atob(this.$route?.query?.tournamentId).replace(
          secret,
          ""
        );
      } catch (error) {
        this.$router.push("not-found");
      }
    }
    this.fetchCities();
    this.fetchGround();
    this.getDetail();
    this.getTournament();
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
      showDelete: false,
      showDeletelogo: false,
      tournamentId: "",
      FullName: "",
      isStart:false,
      FullGroundName:'',
      FullCityName:'',
      FullTournamentName:''
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
        required,
        maxLength: maxLength(100),
        minLength: minLength(2),
      },
      ground: {
        required,
        maxLength: maxLength(100),
        minLength: minLength(2),
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
        required,
      },
      enddate: {
        req: helpers.withMessage(
          "Please select end date.",
          (value) => value != ""
        ),
        dateSameOrAfterStartDate: helpers.withMessage(
          "End date should be the same or after the start date",
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

  const hasLogo = !!this.imageUrl;
  const hasBanner = !!this.bannerUrl;

  const confirmationMessages = {
    '00': "Update tournament without a logo and banner?",
    '01': "Update tournament without a logo?",
    '10': "Update tournament without a banner?",
    '11': "To update tournament details"
  };

  const confirmationText = confirmationMessages[(hasLogo ? '1' : '0') + (hasBanner ? '1' : '0')];

  this.showConfirmationDialog(confirmationText);
},

showConfirmationDialog(confirmationText) {
  Swal.fire({
    title: "Are you sure?",
    text: confirmationText,
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Ok",
    cancelButtonText: "Cancel!",
  }).then((result) => {
    if (result.isConfirmed) {
      this.prepareAndSendFormData();
    }
  });
},
appendLogoToFormData(formData) {
  if (this.imageUrl) {
    if (this.logo) {
      formData.append("logo_url", this.logo);
    }
  } else {
    formData.append("logo_url", "1");
  }
},

appendBannerToFormData(formData) {
  if (this.bannerUrl) {
    if (this.banner) {
      formData.append("banner_url", this.banner);
    }
  } else {
    formData.append("banner_url", "1");
  }
},

prepareAndSendFormData() {
  const formData = new FormData();
  formData.append("name", this.$data.tournament_name);
  formData.append("city", this.$data.city);
  formData.append("ground", this.$data.ground);
  formData.append("start_date", this.$data.startDate);
  formData.append("end_date", this.$data.enddate);
  formData.append("match_type", this.$data.match_type);
  formData.append("ball_type", this.$data.ball_type);
  formData.append("tournament_type", this.$data.category);
  formData.append("description", this.$data.description); 
  this.appendLogoToFormData(formData);
  this.appendBannerToFormData(formData);
  this.updateTour(formData);
}
,
    isStarted(startDate){
      if(startDate <= this.minDate){
        this.isStart=true;
      }
      else{
        this.isStart=false;

      }
    },
    // API call for updating the tournament

    updateTour(formData) {
      updateTournament(this.tournamentId, formData).then(
        () => {
          this.$toast.show("Tournament details updated successfully", {
            type: "success",
          });
          this.$router.push({
            name: "tournament-list",
          });
        },
        () => {  this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });}
      );
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
    preventInput(event) {
      event.preventDefault();
    },
    getDetail() {
      userProfile().then(
        (res) => {
          if (res.data.Name.length <= 20) {
            //if organizer name is less than 20 assign it to organiser_name field
            this.organiser_name = res.data.Name;
          } else {
            //pass the organiser name to the truncateText methos to truncate it
            this.organiser_name = this.truncateText(res.data.Name, 20);
            this.FullName = res.data.Name;
          }
          this.contact = res.data.Phone_Number;
          localStorage.setItem("User_name", res.data.Name);
          localStorage.setItem("Phone_number", res.data.Phone_Number);
        },
        () => {  this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });}
      );
    },
    routes() {
      this.$router.push({
        name: "tournament-list",
      });
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
        // No file selected, retain the previous file name if available
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
        // No file selected, retain the previous file name if available
        if (!this.banner) {
          event.target.value = "";
        }
      }
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
    removeLogo() {
      this.logo = "1";
      this.imageUrl = "";
      const input = document.getElementById("logo");
      if (input) {
        input.value = "";
      }
      this.showDeletelogo = false;
    },
    removeBanner() {
      this.banner = "1";
      this.bannerUrl = "";
      const input = document.getElementById("banner");
      if (input) {
        input.value = "";
      }
      this.showDelete = false;
    },
    getTournament() {
      getTournamentById(this.tournamentId).then(
        (res) => {
          if (res.data.name.length <= 20) {
            this.$data.tournament_name = res.data.name;
          } else {
            this.$data.tournament_name  = this.truncateText(res.data.name, 20);
            this.FullTournamentName = res.data.name;
          }
          if (res.data.city.name.length <= 20) {
            this.$data.city = res.data.city.name;
          } else {
            this.$data.city  = this.truncateText(res.data.city.name, 20);
            this.FullCityName = res.data.city.name;
          }
         
          if (res.data.ground.name.length <= 20) {
            this.$data.ground = res.data.ground.name;
          } else {
            this.$data.ground  = this.truncateText(res.data.ground.name, 20);
            this.FullGroundName = res.data.ground.name;
          }
          this.$data.startDate = res.data.start_date;
          this.$data.enddate = res.data.end_date;
          this.$data.match_type = res.data.match_type;
          this.$data.ball_type = res.data.ball_type;
          this.$data.category = res.data.tournament_type;
          this.$data.description = res.data.description;
          this.isStarted(res.data.start_date);
          try {
            if (res.data.logo_url) {
              this.showDeletelogo = true;
              this.$data.imageUrl = require(`../assets${res.data.logo_url}`);
            }
          } catch (error) {
            this.$data.imageUrl = `${process.env.VUE_APP_FILE_PATH}${res.data.logo_url}`;
          }
          try {
            if (res.data.banner_url) {
              this.showDelete = true;
              this.$data.bannerUrl = require(`../assets${res.data.banner_url}`);
            }
          } catch (error) {
            this.$data.bannerUrl = `${process.env.VUE_APP_FILE_PATH}${res.data.banner_url}`;
          }
        },
        () => {
          this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });
        }
      );
    },
    truncateText(text, limit) {
      if (text.length > limit) {
        return text.slice(0, limit) + "...";
      }
      return text;
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
