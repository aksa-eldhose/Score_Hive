<template>
    <NavBar />
   <div class="form-wrap">
     <h3 class="text-start" style="letter-spacing: 1px">
       Update Match
     </h3>
     <hr />
     
<div class="row">
 <div class="col-md-6">
    <div class="form-group">
             <label
               >{{ $t("Round")
               }}<span class="required">*</span></label
             >
             <input
               type="text"
               class="form-control"
               v-model.trim="round"
               disabled
             />
           </div>
 </div>
 <div class="col-md-6">
    <div class="form-group">
             <label
               >{{ $t("Group")
               }}<span class="required">*</span></label
             >
             <input
               type="text"
               class="form-control"
               v-model.trim="group"
               disabled
             />
           </div>
 </div>
</div>
<div class="row mt-4">
 <div class="col-md-6">
    <div class="form-group">
             <label
               >{{ $t("Team_A")
               }}<span class="required">*</span></label
             >
             <input
               type="text"
               class="form-control"
               v-model.trim="teamA"
               disabled
             />
           </div>
 </div>
 <div class="col-md-6">
    <div class="form-group">
             <label
               >{{ $t("Team_B")
               }}<span class="required">*</span></label
             >
             <input
               type="text"
               class="form-control"
               v-model.trim="teamB"
               disabled
             />
           </div>
 </div>
 <div class="row mt-4">
 <div class="form-group">
   <label style="margin-right: 5px;">{{ $t("Match_Type") }}<span class="required">*</span></label>&nbsp;
   <div class="custom-control custom-checkbox custom-control-inline mt-1">
     <input
       type="radio"
       class="custom-control-input"
       name="match_type"
       value="0"
       id="yes"
       checked="true"
       v-model="match_type"
     />
     &nbsp;<label class="custom-control-label" for="yes" style="margin-right: 5px;">{{ $t("Limited") }}</label>
     <input
       type="radio"
       class="custom-control-input"
       value="1"
       v-model="match_type"
       style="margin-left: 15px;"
     />
     &nbsp;<label class="custom-control-label" for="no">{{ $t("Test") }}</label>
   </div>
 </div>
</div>

<div class="row">
 <div class="col-md-6" v-if="match_type === '0'"> <!-- Show only when 'Limited' option is selected -->
   <div class="form-group mt-4">
     <label>{{ $t("No_of_overs") }}<span class="required">*</span></label>
     <input
       type="text"
       placeholder="Enter the number of overs"
       class="form-control"
       v-model.trim="noOfOver"
     />
     <span v-if="v$?.noOfOver.$dirty">
 <span v-for="(error, index) in v$?.noOfOver?.$errors" :key="index" class="text-danger fs-7">
   <span v-if="error.$params.type === 'required'">
     <small>Please enter the number of overs</small><br>
   </span>
   <span v-else-if="error.$params.type === 'minValue' || error.$params.type === 'maxValue'|| error.$params.type === 'numeric'">
     <small v-if="index === 0">Please enter a numeric value between 1 and 99</small>
   </span>
 </span>
</span>


   </div>
 </div>
 <div class="col-md-6" v-if="match_type === '0'"> <!-- Show only when 'Limited' option is selected -->
   <div class="form-group mt-4">
     <label>{{ $t("Overs_Per_Bowler") }}<span class="required">*</span></label>
     <input
       type="text"
       placeholder="Enter the overs per bowler"
       class="form-control"
       v-model.trim="overPerBowler"
     />
     <span v-if="v$?.overPerBowler.$dirty">
 <span v-for="(error, index) in v$?.overPerBowler?.$errors" :key="index" class="text-danger fs-7">
   <span v-if="error.$params.type === 'required'">
     <small>Please enter the number of overs per bowler</small><br>
   </span>
   <span v-else-if="error.$params.type === 'minValue' || error.$params.type === 'maxValue'|| error.$params.type === 'numeric'">
     <small v-if="index === 0">Please enter a numeric value between 1 and 20</small>
   </span>
 </span>
</span>
   </div>
 </div>
</div>

<div class="row">
   <div class="col-md-4">
           <div class="form-group mt-4">
             <label
               >{{ $t("City_or_Town")
               }}<span class="required">*</span></label
             >
             <input
               type="text"
               placeholder="Enter the city or town"
               class="form-control"
               v-model.trim="city"
             />
              <span
               v-for="(error, index) in v$?.city?.$errors" :key="index"
               class="text-danger fs-7"
             >
               <small>{{ error.$message }}</small>
             </span>
           </div>
         </div>
         <div class="col-md-4">
           <div class="form-group mt-4">
             <label
               >{{ $t("Ground")
               }}<span class="required">*</span></label
             >
             <input
               type="text"
               placeholder="Enter the ground"
               class="form-control"
               v-model.trim="ground"
             />
             <span
               v-for="(error, index) in v$?.ground?.$errors" :key="index"
               class="text-danger fs-7"
             >
               <small>{{ error.$message }}</small>
             </span>
           </div>
         </div>
         <div class="col-md-4">
           <div class="form-group mt-4">
             <label
               >{{ $t("Date_&_Time")
               }}<span class="required">*</span></label
             >
             <input
               type="datetime-local"
               class="form-control"
               v-model.trim="dateTime"
               @keydown="preventInput"
             />
             <span
               v-for="(error, index) in v$?.dateTime?.$errors" :key="index"
               class="text-danger fs-7"
             >
               <small>{{ error.$message }}</small>
             </span>
           </div>
         </div>
</div>
<div class="row">
   <ButtonComponent
             class="btn btn-primary mt-4"
             type="button"
             color="primary"
             @click="submit()"
             style="width: 8%;margin-left: 10px;"
             :disabled="isLoading"
           >
             <span
               v-if="isLoading"
               class="spinner-border spinner-border-sm me-2"
               role="status"
               aria-hidden="true"
             ></span>
             <span v-else
               ><span>{{ $t("UPDATE") }}</span></span
             ></ButtonComponent
           >
           <ButtonComponent
             type="button"
             color="white"
             class="btn btn-outline-primary mt-4"
             @click="routes()"
             style="width: 8%;margin-left: 10px;"
           >
             {{ $t("CANCEL") }}
           </ButtonComponent>
</div>
</div>
</div>
</template>
<script>
import NavBar from "./NavBar.vue";
import ButtonComponent from "@/components/Button.vue";
import { useVuelidate } from "@vuelidate/core";
import { required, maxLength, minLength,minValue,maxValue,numeric,helpers} from "@vuelidate/validators";
export default {
   components: {
   NavBar,
   ButtonComponent
 },
 data() {
   return {
    round:'LEAGUE',
    group:'GROUP A',
    teamB:'TEAM 1',
    teamA:'TEAM 2',
    match_type: "0",
    noOfOver:'20',
    overPerBowler:'4',
    city:'Delhi',
    ground:'ABC Ground',
    dateTime:'2023-12-12 12:00:00',
    isLoading:false,
    tournamentId:''
   };
 },
 setup() {
   return { v$: useVuelidate() };
 },
 mounted(){
  if (this.$route?.params?.TournamentId) {
      const secret = "tournamentUpdate";
      try {
        this.tournamentId = atob(this.$route?.params?.TournamentId).replace(
          secret,
          ""
        );
      } catch (error) {
        this.$router.push("not-found");
      }
    }
 },
 computed:{
   teamsMatch() {
     if(this.teamB ===''){
       return true
     }
     else{
       return this.teamA != this.teamB;
     }
   },
 },
 validations() {
   return {
       round: {
       required
     },
     group:{
       required
     },
     teamA:{
       required
     },
     teamB:{
       required,
     },
     noOfOver: {
       required,
       minValue: minValue(1),
       maxValue: maxValue(99),
       numeric
   },
   overPerBowler: {
       required,
       minValue: minValue(1),
       maxValue: maxValue(20),
       numeric
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
       req: helpers.withMessage(
         "Please enter city.",
         (value) => value != ""
       ),
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
     dateTime:{
       req: helpers.withMessage(
         "Please select date and time.",
         (value) => value != ""
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
     }
   };
 },
 methods: {
   async submit() {
     const isValid = await this.v$.$validate();
     if (isValid) {
       this.isLoading=true;
       this.$toast.success("Updated successfully....!!");
       setTimeout(() => {
             this.isLoading = false; // Set isLoading to false after a delay
           }, 1000);

     }
     else{
       this.isLoading=false
     }
    
   },
   routes(){
    const encodedId = btoa(this.tournamentId + "tournamentMatch");
      this.$router.push({
        name: "match-list",
        params: { TournamentId: encodedId },
      });
   },
}
}
</script>

<style scoped>
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
.required{
   color: red;
}

</style>