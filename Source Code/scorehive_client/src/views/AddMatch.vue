<template>
  <NavBar />
  <div class="form-wrap">
    <h3 class="text-start" style="letter-spacing: 1px">Schedule Match</h3>
    <hr />

    <div class="row">
      <div class="col-md-6">
        <!--for round-->
        <div class="form-group">
          <label>Round<span class="required">*</span></label>
          <select class="select form-select round" v-model.trim="selectedRound">
            <option disabled value="">Select round</option>
            <option v-for="item in round" :key="item.id" :value="item.round_id">{{ item.name }}</option>
          </select>
          <!--Validations-->
          <div
            v-for="error of v$.selectedRound.$errors"
            :key="error"
            class="text-danger round"
            id="requiredData"
          >
            <span v-if="error.$params.type == 'required'">
              <small>Please select the round.</small>
            </span>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <!--for group-->
        <div class="form-group">
          <label>Group<span class="required">*</span></label>
          <select class="select form-select" v-model.trim="selectedGroup" @change="onChange($event)">
            <option disabled selected value>Select group</option>
            <option v-for="item in group" :key="item" :value="item.id">{{ item.name }}</option>
          </select>
          <!--Validations-->
          <div
            v-for="error of v$.selectedGroup.$errors"
            :key="error"
            class="text-danger"
            id="requiredData"
          >
            <span v-if="error.$params.type == 'required'">
              <small>Please select the group.</small>
            </span>
          </div>
        </div>
      </div>
    </div>
    <div class="row mt-4">
      <div class="col-md-6">
        <!--for first team-->
        <div class="form-group">
          <label>Team A<span class="required">*</span></label>
          <select class="select form-select" v-model.trim="teamA" :disabled="!selectedGroup">
            <option disabled selected value>Select team A</option>
            <option v-for="team in teams" :key="team" :value="team.team">{{ team.name }}</option>
          </select>
          <!--Validations-->
          <div
            v-for="error of v$.teamA.$errors"
            :key="error"
            class="text-danger"
            id="requiredData"
          >
            <span v-if="error.$params.type == 'required'">
              <small>Please select the team.</small>
            </span>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <!--for second team-->
        <div class="form-group">
          <label>Team B<span class="required">*</span></label>
          <select class="select form-select" v-model.trim="teamB" :disabled="!selectedGroup">
            <option disabled selected value>Select team B</option>
            <option v-for="team in teams" :key="team" :value="team.team">{{ team.name }}</option>
          </select>
          <!--Validations-->
          <div
            v-for="error of v$.teamB.$errors"
            :key="error"
            class="text-danger"
            id="requiredData"
          >
            <span v-if="error.$params.type == 'required'">
              <small>Please select the team.</small>
            </span>
          </div>
          <span v-if="!teamsMatch" class="text-danger" id="teamsNotMatch">
            <small>Team A and Team B cannot be the same</small>
          </span>
        </div>
      </div>
      <div class="row mt-4">
        <!--for choosing match type-->
        <div class="form-group">
          <label style="margin-right: 5px"
            >{{ $t("Match_Type") }}<span class="required">*</span></label
          >&nbsp;
          <div
            class="custom-control custom-checkbox custom-control-inline mt-1"
          >
            <input
              type="radio"
              class="custom-control-input"
              name="match_type"
              value="0"
              id="yes"
              checked="true"
              v-model="match_type"
            />
            &nbsp;<label
              class="custom-control-label"
              for="yes"
              style="margin-right: 5px"
              >{{ $t("Limited") }}</label
            >
            <input
              type="radio"
              class="custom-control-input"
              value="1"
              v-model="match_type"
              style="margin-left: 15px"
            />
            &nbsp;<label class="custom-control-label" for="no">{{
              $t("Test")
            }}</label>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6" v-if="match_type === '0'">
          <!-- Show only when 'Limited' option is selected -->
          <div class="form-group mt-4">
            <label
              >{{ $t("No_of_overs") }}<span class="required">*</span></label
            >
            <input
              type="text"
              placeholder="Enter the number of overs"
              class="form-control noOver"
              v-model.trim="noOfOver"
            />
            <!--Validations-->
            <span v-if="v$?.noOfOver.$dirty">
              <span
                v-for="(error, index) in v$?.noOfOver?.$errors"
                :key="index"
                class="text-danger noOver fs-7 "
              >
                <span v-if="error.$params.type === 'required'">
                  <small>Please enter the number of overs</small><br />
                </span>
                <span
                  v-else-if="
                    error.$params.type === 'minValue' ||
                    error.$params.type === 'maxValue' ||
                    error.$params.type === 'numeric'
                  "
                  id="numericValue"
                >
                  <small v-if="index === 0"
                    >Please enter a numeric value between 1 and 99</small
                  >
                </span>
              </span>
            </span>
          </div>
        </div>
        <div class="col-md-6" v-if="match_type === '0'">
          <!-- Show only when 'Limited' option is selected -->
          <div class="form-group mt-4">
            <label
              >{{ $t("Overs_Per_Bowler")
              }}<span class="required">*</span></label
            >
            <input
              type="text"
              placeholder="Enter the overs per bowler"
              class="form-control"
              v-model.trim="overPerBowler"
            />
            <!--Validations-->
            <span v-if="v$?.overPerBowler.$dirty">
              <span
                v-for="(error, index) in v$?.overPerBowler?.$errors"
                :key="index"
                class="text-danger fs-7"
              >
                <span v-if="error.$params.type === 'required'">
                  <small>Please enter the number of overs per bowler</small
                  ><br />
                </span>
                <span
                  v-else-if="
                    error.$params.type === 'minValue' ||
                    error.$params.type === 'maxValue' ||
                    error.$params.type === 'numeric'
                  "
                  id="numericValue"
                >
                  <small v-if="index === 0"
                    >Please enter a numeric value between 1 and 20</small
                  >
                </span>
              </span>
            </span>
          </div>
        </div>
      </div>

      <div class="row">
        <!--Input for city-->
        <div class="col-md-4">
          <div class="form-group mt-4">
            <label
              >{{ $t("City_or_Town") }}<span class="required">*</span></label
            >
            <input
              type="text"
              placeholder="Enter the city or town"
              class="form-control"
              v-model.trim="city"
            />
            <!--Validations-->
            <span
              v-for="(error, index) in v$?.city?.$errors"
              :key="index"
              class="text-danger fs-7"
              id="requiredData"
            >
              <small>{{ error.$message }}</small>
            </span>
          </div>
        </div>
        <div class="col-md-4">
          <!--Validations-->
          <div class="form-group mt-4">
            <label>{{ $t("Ground") }}<span class="required">*</span></label>
            <input
              type="text"
              placeholder="Enter the ground"
              class="form-control"
              v-model.trim="ground"
            />
            <!--Validations-->
            <span
              v-for="(error, index) in v$?.ground?.$errors"
              :key="index"
              class="text-danger fs-7"
              id="requiredData"
            >
              <small>{{ error.$message }}</small>
            </span>
          </div>
        </div>
        <div class="col-md-4">
          <!--Input for adding date and time-->
          <div class="form-group mt-4">
            <label
              >{{ $t("Date_&_Time") }}<span class="required">*</span></label
            >
            <input
              type="datetime-local"
              class="form-control"
              v-model.trim="dateTime"
              @keydown="preventInput"
            />
            <!--Validations-->
            <span
              v-for="(error, index) in v$?.dateTime?.$errors"
              :key="index"
              class="text-danger fs-7"
              id="dateTime"
            >
              <small>{{ error.$message }}</small>
            </span>
          </div>
        </div>
      </div>
      <div class="row">
        <!--Submit button.Calls the submit method on click-->
        <ButtonComponent
          class="btn btn-primary mt-4"
          id="submitButton"
          type="button"
          color="primary"
          @click="submit()"
          style="width: 8%; margin-left: 10px"
          :disabled="isLoading"
        >
          <span
            v-if="isLoading"
            class="spinner-border spinner-border-sm me-2"
            role="status"
            aria-hidden="true"
          ></span>
          <span v-else
            ><span>{{ $t("Submit") }}</span></span
          ></ButtonComponent
        >
        <!--Cancel button.Calls the routes method on click-->
        <ButtonComponent
          type="button"
          color="white"
          class="btn btn-outline-primary mt-4"
          @click="routes()"
          style="width: 8%; margin-left: 10px"
        >
          {{ $t("CANCEL") }}
        </ButtonComponent>
      </div>
    </div>
  </div>
</template>
<script>
import Swal from "sweetalert2";
import errorCodes from "@/services/errorCodes.json";
import { GroupList,GroupDetailsById} from "@/services/groupService";
import { scheduleMatch } from "@/services/matchService";
import { tournamentRoundList } from "@/services/roundService";
import NavBar from "./NavBar.vue";
import ButtonComponent from "@/components/Button.vue";
import { useVuelidate } from "@vuelidate/core";
import {
  required,
  maxLength,
  minLength,
  minValue,
  maxValue,
  numeric,
  helpers,
  requiredIf
} from "@vuelidate/validators";
export default {
  components: {
    NavBar,
    ButtonComponent,
  },
  data() {
    return {
      round: [],
      selectedRound: '',
      group: [],
      selectedGroup: '',
      teamB: "",
      teamA: "",
      match_type: "0",
      noOfOver: "",
      overPerBowler: "",
      city: "",
      ground: "",
      dateTime: "",
      isLoading: false,
      tournamentId:'',
      teams:[]
    };
  },
  setup() {
    return { v$: useVuelidate() };
  },
  mounted(){
    if (this.$route?.params?.TournamentId) {
      const secret = "tournamentSchdedule";
      try {
        this.tournamentId = atob(this.$route?.params?.TournamentId).replace(
          secret,
          ""
        );
      } catch (error) {
        this.$router.push("not-found");
      }
    }
    this.getGroupList();
    this. getRounds();
  },
  computed: {
    teamsMatch() {//checks if the team A and Team b are same
      if (this.teamB === "") {
        return true;
      } else {
        return this.teamA != this.teamB;
      }
    },
  },
  validations() {//validations for each input field
    return {
      selectedRound: {
        required,
      },
      selectedGroup: {
        required,
      },
      teamA: {
        required,
      },
      teamB: {
        required,
      },
      noOfOver: {
        required: requiredIf(function () {
        return this.match_type === 0;
      }),
        minValue: minValue(1),
        maxValue: maxValue(99),
        numeric,
      },
      overPerBowler: {
        required: requiredIf(function () {
        return this.match_type === 0;
      }),
        minValue: minValue(1),
        maxValue: maxValue(20),
        numeric,
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
          (value) => value !=""
        ),
      },
      dateTime: {
        req: helpers.withMessage(
          "Please select date and time.",
          (value) => value !=""
        ),
        noPastValue: helpers.withMessage(
          "Past time and date are not allowed",
          (value) => {
            if (!value) return true; // Skip validation if the field is empty
            const selectedDate = new Date(value);
            const now = new Date();
            return selectedDate >= now;
          }
        ),
      },
    };
  },
  methods: {
    onChange(event) {
      GroupDetailsById(event.target.value).then(
        (response) => {
          this.teams=response.data.teams
          if(this.teams.length===0){//check if the selected groups have any teams
            Swal.fire({
                  icon: "error",
                  title: "Failed",
                  text: "The selected group does not have any teams",
                });
          }
        },
        () => {
          this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          });        }
      );
      this.getGroupList();
          },
    async submit() {//method to call the schedule match api
      const isValid = await this.v$.$validate();
      if (isValid && this.teamsMatch) {//chekcs if all the input fields are valid
        // this.isLoading = true;
        if(this.match_type==1){
          this.overPerBowler=0
          this.noOfOver=0
        }
        let param=
        {
              "tournament_id":+this.tournamentId,
              "team1":this.teamA,
              "team2":this.teamB,
              "match_type":this.match_type,
              "date_time":this.dateTime,
              "round_id":this.selectedRound,
              "over_per_bowler":+this.overPerBowler,
              "total_overs":+this.noOfOver,
              "city": this.city,
              "ground": this.ground
        }
        scheduleMatch(param).then(
        () => {
         this.$toast.success("Added successfully....!!");
         this.routes();
        setTimeout(() => {
          this.isLoading = false; // Set isLoading to false after a delay
        }, 1000);
        },
        (error) => {
          const errorMessage =
                  errorCodes[error.response.data.error_code] ||
                  "Oops.. Some unknown error occurred..!";
        this.$toast.error(errorMessage);
              setTimeout(() => {
          this.isLoading = false; // Set isLoading to false after a delay
        }, 1000);
        }
      );
      } else {
        this.isLoading = false;
      }
    },
    getGroupList() {
      this.teamA=''
      this.teamB=''
      GroupList(this.tournamentId).then(
        (response) => {
          this.group=response.data
        },
        (error) => {
          if(error.response.data.error_code == 1039){
            this.$router.push("not-found");
          }
          if(error.response.data.error_code ==4014){
            Swal.fire({
                  icon: "error",
                  title: "Failed",
                  text: "There are no groups added to the tournament.Please add group first.",
                });
              const encodedId = btoa(this.tournamentId  + "tournamentGroups");
              this.$router.push({
                name: "group",
                params: { TournamentId: encodedId },
              });
          }
        }
      );
    },
    routes() {//method to reset the form
      const encodedId = btoa(this.tournamentId + "tournamentMatch");
      this.$router.push({
        name: "match-list",
        params: { TournamentId: encodedId },
      });
    },
    getRounds(){
      tournamentRoundList(this.tournamentId).then(
        (response) => {
          this.round=response.data.results
          if(this.round.length===0){//check if the selected groups have any teams
            Swal.fire({
                  icon: "error",
                  title: "Failed",
                  text: "There are no rounds added to the tournament.Please add rounds first",
                });
                const encodedId = btoa(this.tournamentId + "tournamentRounds");
                this.$router.push({
                  name: "list-rounds",
                  params: { TournamentId: encodedId },
                });
          }
        },
        () => {
          this.$toast.show("Oops.. Some unknown error occurred..!", {
            type: "error",
          }); 
        }
      );
    }
  },
};
</script>
<style scoped>
.form-wrap {
  background: rgb(255, 255, 255);
  width: 100%;
  max-width: 1100px;
  padding: 50px;
  margin-inline:  auto;
  margin-bottom: 5%;
  margin-top: 3%;
  box-shadow: 0px 0px 40px rgba(0, 0, 0, 0.15);
}
.required {
  color: red;
}
</style>
