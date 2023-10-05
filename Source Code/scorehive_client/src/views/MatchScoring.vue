<template>
  <NavBar /><!-- Add the Bootstrap Icons CSS in the <head> section of your HTML -->
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0@beta1/dist/css/bootstrap.min.css"
    rel="stylesheet"
  />

  <div class="position-relative overlay">
    <div class="img-card">
      <div class="position-absolute top-10 left-10 w-100 h-100">
        <img :src="emptytournament" alt="" />
      </div>
    </div>
    <div
      style="z-index: 10"
      class="position-absolute top-50 start-50 translate-middle"
    >
      <!-- Part 1 -->
      <div class="d-flex justify-content-center">
        <div>
          <div class="d-flex align-items-center justify-content-center">
            <LogoContainer
              :showImage="logo !== 1"
              :imageUrl="imageUrl || logo"
              :emptyImageContent="emptyImageContent"
              containerWidth="150px"
              containerHeight="150px"
              borderRadius="50%"
              style="z-index: 10"
            />

            <p class="text-center px-4 overlay-text">
              <b class="fs-3 fw-bold px-3"
                >{{ totalRunsScored }}/{{ totalWickets }}</b
              ><br />

              <span class="fs-5 fw-bold">{{ team }}</span>
              <b class="fs-3 fw-bold px-3">VS</b>

              <span class="fs-5 fw-bold">{{ nonSelectedTeam }}</span>
            </p>
            <div class="d-flex align-items-center">
              <LogoContainer
                :showImage="logo !== 1"
                :imageUrl="imageUrl || logos"
                :emptyImageContent="emptyImageContent"
                containerWidth="150px"
                containerHeight="150px"
                borderRadius="50%"
                style="z-index: 10"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <br />
  <div class="container">
    <div class="form-wrap">
      <form @submit.prevent>
        <span
          class="batsman-info"
          v-if="this.id != nonSelectedId"
          style="z-index: 100"
        >
          {{ team }}
          <img
            src="https://images.vexels.com/media/users/3/240076/isolated/preview/0e6c0d8799dc06d116bd376820a6b091-cricket-bat-player-cut-out.png"
            alt="Cricket Bat Icon"
            width="60"
            height="60"
          />
        </span>
        <span class="batsman-info" v-if="this.id == nonSelectedId">
          {{ nonSelectedTeam }}
          <img
            src="https://images.vexels.com/media/users/3/240076/isolated/preview/0e6c0d8799dc06d116bd376820a6b091-cricket-bat-player-cut-out.png"
            alt="Cricket Bat Icon"
            width="60"
            height="60"
          />
        </span>
        <div class="info-box">
          <div
            v-for="(batsman, index) in batsmen"
            :key="index"
            class="batsman-info"
          >
            {{ batsman.name }} {{ batsman.runs }}/({{ batsman.ballsFaced }})

            <span v-if="currentBatterIndex === index" class="required">
              <img
                src="https://images.vexels.com/media/users/3/240076/isolated/preview/0e6c0d8799dc06d116bd376820a6b091-cricket-bat-player-cut-out.png"
                alt="Cricket Bat Icon"
                width="60"
                height="60"
              />
            </span>
          </div>
        </div>
        <div class="info-box">
          <!-- Batsman name and runs -->
          <div class="row w-100">
            <div
              class="col-md-3 batsman-info text-start"
              v-if="bowlerlist && bowlerlist.length > 0"
            >
              <img
                src="https://cdn-icons-png.flaticon.com/256/1454/1454436.png"
                alt="Cricket Bat Icon"
                width="40"
                height="40"
              />
              {{ bowlerlist[0].name }}
              {{ totalBalls }}
            </div>
            <div class="col-md-9 batsman-info text-end">
              <span v-if="completedOvers.length > 0" class="text-success">
                Completed Overs:
                {{
                  completedOvers
                    .map((over) =>
                      over
                        .map((balls, index) => {
                          const ballValue = balls.value;
                          const ballType = balls.balltype;

                          if (ballType === "NM" && over.length === 6) {
                            return ballValue;
                          } else if (ballType === "NB") {
                            return ballValue + " NB";
                          } else if (ballType === "WD") {
                            return ballValue + " WD";
                          } else if (ballType === "LB") {
                            return ballValue + " LB";
                          } else {
                            return ballValue;
                          }
                        })
                        .join("-")
                    )
                    .join(" | ")
                }} </span
              ><br />
              <span v-if="overHistory.length > 0" class="text-primary">
                This Over:{{
                  overHistory
                    .map((balls, index) => {
                      if (balls.balltype === "NM" && overHistory.length === 6) {
                        return balls.value;
                      } else if (balls.balltype === "NB") {
                        return balls.value + " NB";
                      } else if (balls.balltype === "WD") {
                        return balls.value + " WD";
                      } else if (balls.balltype === "LB") {
                        return balls.value + " LB";
                      } else {
                        return balls.value;
                      }
                    })
                    .join("-")
                }}
              </span>
            </div>
          </div>

          <!-- Bowler name and number of bowls -->
        </div>
        <div class="calculator-grid">
          <!-- Row 1 -->
          <button
            @click="updateScore(0)"
            class="btn btn-primary btn-square"
            :disabled="isDisabled"
          >
            0
          </button>
          <button
            @click="updateScore(1)"
            class="btn btn-primary btn-square"
            :disabled="isDisabled"
          >
            1
          </button>
          <button
            @click="updateScore(2)"
            class="btn btn-primary btn-square"
            :disabled="isDisabled"
          >
            2
          </button>
          <button
            @click="updateScore(3)"
            class="btn btn-primary btn-square"
            :disabled="isDisabled"
          >
            3
          </button>

          <!-- Row 2 -->

          <button
            @click="updateScore(4)"
            class="btn btn-primary btn-square"
            :disabled="isDisabled"
          >
            4
          </button>
          <button
            @click="updateScore(5)"
            class="btn btn-primary btn-square"
            :disabled="isDisabled"
          >
            5
          </button>
          <button
            @click="updateScore(6)"
            class="btn btn-primary btn-square"
            :disabled="isDisabled"
          >
            6
          </button>

          <!-- Row 3 -->
          <button
            @click="undoLastBall()"
            class="btn btn-warning btn-square"
            :disabled="isDisabled"
          >
            UNDO
          </button>
          <button
            @click="openModal('LB')"
            class="btn btn-info btn-square"
            :disabled="isDisabled"
          >
            LB
          </button>
          <button
            @click="openModal('NB')"
            class="btn btn-info btn-square"
            :disabled="isDisabled"
          >
            NB
          </button>

          <!-- Row 4 -->
          <button
            @click="openModal('WD')"
            class="btn btn-info btn-square"
            :disabled="isDisabled"
          >
            WD
          </button>

          <button
            @click="performOut()"
            class="btn btn-danger btn-square"
            :disabled="isDisabled"
          >
            OUT
          </button>
          <!-- Add more buttons as needed -->
        </div>
      </form>
      <Modal
        :show="modalOpen"
        @close="closeModal"
        class="modalContent"
        :disabled="isDisabled"
      >
        <div class="d-flex align-items-center mb-3">
          <input
            type="text"
            name="name"
            id="name"
            placeholder="Runs"
            class="form-control"
            v-model.trim="runsByStriker"
            v-if="wideNoBallFlag"
          />
          <input
            type="text"
            name="name"
            id="name"
            placeholder="Extras"
            class="form-control"
            v-model.trim="extras"
            v-if="legByFlag"
          />
          &nbsp;
          <cbutton
            style="width: 100px; height: 36px"
            color="primary"
            @click="extraScore(runsByStriker, extras)"
            >Add</cbutton
          >
        </div>
        <div v-if="wideNoBallFlag">
          <div
            v-for="error of v$.runsByStriker.$errors"
            :key="error"
            class="error"
          >
            <span v-if="error.$params.type === 'required'"
              >Please enter the runs</span
            >
            <span v-if="error.$params.type == 'numeric'"
              >Please enter a numeric value</span
            >
          </div>
        </div>
        <div v-if="legByFlag">
          <div v-for="error of v$.extras.$errors" :key="error" class="error">
            <span v-if="error.$params.type === 'required'"
              >Please enter the extra run</span
            >
            <span v-if="error.$params.type == 'numeric'"
              >Please enter a numeric value</span
            >
          </div>
        </div>
      </Modal>
    </div>
  </div>
</template>
<script>
import NavBar from "./NavBar.vue";
import emptytournament from "@/assets/img/scoring.jpg";
import logo from "@/assets/img/logo1.jpg";
import logos from "@/assets/img/logo2.jpg";
import "bootstrap-icons/font/bootstrap-icons.css";
import LogoContainer from "@/components/LogoContainer.vue";
import Modal from "../components/ModalComponent.vue";
import cbutton from "@/components/Button.vue";
import { useVuelidate } from "@vuelidate/core";
import { required, numeric } from "@vuelidate/validators";
import { saveScore } from "@/services/matchService";
import errorCodes from "@/services/errorCodes.json";
import { playerList } from "@/services/playerService";
import Swal from "sweetalert2";
export default {
  components: {
    NavBar,
    LogoContainer,
    Modal,
    cbutton,
  },
  setup() {
    return { v$: useVuelidate() };
  },
  data() {
    return {
      emptytournament,
      logos,
      logo,
      name: "",
      batsmen: [],
      overHistory: [],
      currentBatterIndex: 0,
      modalOpen: false,
      extras: "",
      extrasArray: [],
      runsByStriker: "",
      completedOvers: [],
      extraScoreStatus: "",
      showExtrasInput: "",
      showWideInput: "",
      totalRuns: [],
      total: 0,
      legByFlag: false,
      wideNoBallFlag: false,
      previousBatsman: 0,
      temp: 0,
      temp1: 0,
      match_id: "",
      over: "",
      ball_number: "",
      striker_id: "",
      non_striker_id: "",
      bowler_id: "",
      runs: "",
      is_wicket: "",
      playerlist: [],
      ballNumber: 0,
      inning: 1,
      bowlerlist: [],
    };
  },
  validations() {
    return {
      runsByStriker: {
        required,
        numeric,
      },
      extras: {
        required,
        numeric,
      },
    };
  },

  computed: {
    totalRunsScored() {
      const allData = this.completedOvers.flat();
      const totalRuns = allData.reduce((sum, data) => sum + data.value, 0);
      const updatedTotal = this.overHistory.reduce(
        (total, ballData) => total + ballData.value,
        0
      );
      const totals = updatedTotal + totalRuns;
      return totals;
    },
    totalWickets() {
      return (
        this.overHistory.filter((overballData) => overballData.out).length +
        this.completedOvers.flat().filter((overballData) => overballData.out)
          .length
      );
    },
    totalBalls() {
      const totalBallsInOverHistory = this.overHistory.reduce((total) => {
        return total + 1;
      }, 0);
      const totalBallsInCompletedOvers = this.completedOvers
        .flat()
        .reduce((totalBalls) => {
          return totalBalls + 1;
        }, 0);
      return totalBallsInOverHistory + totalBallsInCompletedOvers;
    },
    isDisabled() {
      return (
        this.batsmen.length === 0 &&
        this.overHistory.length === 0 &&
        this.completedOvers.length === 0
      );
    },
  },
  mounted() {
    if (this.$route?.params?.MatchId) {
      const secret = "tournamentMatch";
      try {
        this.MatchId = atob(this.$route?.params?.MatchId).replace(secret, "");
        this.tournamentId = atob(this.$route?.params?.tournamentId).replace(
          secret,
          ""
        );
        this.team = atob(this.$route?.params?.team).replace(secret, "");
        this.team = atob(this.$route?.params?.team).replace(secret, "");
        this.id = atob(this.$route?.params?.id).replace(secret, "");
        this.nonSelectedId = atob(this.$route?.params?.nonSelectedId).replace(
          secret,
          ""
        );
        this.nonSelectedTeam = atob(
          this.$route?.params?.nonSelectedTeam
        ).replace(secret, "");
        this.category = atob(this.$route?.params?.category).replace(secret, "");
      } catch (error) {
        this.$router.push("not-found");
      }
    }
    this.playerList();
    this.bowlerList();
  },
  methods: {
    async matchScoring() {
      const paramsArray = this.overHistory.map((over) => ({
        match_id: Number(this.MatchId),
        batting_team: Number(over.teamid),
        inning: this.inning,
        over: over.over, // Calculate over number
        ball_number: over.ballNumber, // Calculate ball number within over
        striker_id: over.id,
        bowler_id: this.bowlerlist[0].player_id, // Update with the appropriate bowler ID
        runs: over.runs,
        is_wicket: over.out ? 1 : 0, // Set 1 if out, otherwise 0
      }));

      saveScore(paramsArray).then(
        () => {
          this.$toast.show("Score Saved..!", {
            type: "success",
          });
        },
        (error) => {
          const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
        }
      );
    },
    bowlerList() {
      playerList(this.nonSelectedId).then(
        (response) => {
          this.bowlerlist = response.data;
          this.length = response.data.length;
          // Populate the batsmen array with id and name from playerlist
        },
        (error) => {
          const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
        }
      );
    },
    playerList() {
      playerList(this.id).then(
        (response) => {
          this.playerlist = response.data;
          this.length = response.data.length;
          if (this.length != 0) {
            if (this.length != 0) {
              this.batsmen = [];
              this.player1 = this.playerlist.pop();
              this.batsmen = [
                {
                  teamid: this.id,
                  id: this.player1.player_id,
                  name: this.player1.name,
                  runs: 0,
                  ballsFaced: 0,
                  current: false,
                },
              ];
              this.player2 = this.playerlist.pop();
              this.batsmen.push({
                teamid: this.id,
                id: this.player2.player_id,
                name: this.player2.name,
                runs: 0,
                ballsFaced: 0,
                current: false,
              });
            }
          }
        },
        (error) => {
          const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
        }
      );
    },
    updateScore(value) {
      if (typeof value === "number") {
        const currentBatter = this.batsmen[this.currentBatterIndex];
        this.previousBatsman = this.currentBatterIndex;
        currentBatter.runs += value;
        currentBatter.ballsFaced++;
        this.overHistory.push({
          batsman: this.currentBatterIndex,
          id: currentBatter.id,
          match_id: Number(this.MatchId),
          teamid: currentBatter.teamid,
          value: value,
          over: Math.floor(this.totalBallss() / 6) + 1,
          balltype: "NM",
          name: currentBatter.name,
          runs: currentBatter.runs,
          balls: currentBatter.ballsFaced,
          ballNumber: this.totalBallsInOverHistory() + 1,
        });
        if (value % 2 != 0) {
          this.swapBatsmen();
        }
      }
      const balltypeToCount = "NM";
      const filteredData = this.overHistory.filter(
        (item) => item.balltype === balltypeToCount
      );
      let overLength = filteredData.length;
      if (overLength > 6) {
        this.temp1 = this.overHistory.pop();
        this.matchScoring();
        this.completedOvers.push(this.overHistory);
        this.overHistory = [];
        this.overHistory.push(this.temp1);
      }
    },

    swapBatsmen() {
      // Swapping just changes the currentBatterIndex to the other batsman
      this.currentBatterIndex = 1 - this.currentBatterIndex;
    },
    performOut() {
      if (this.batsmen.length > 0) {
        // Remove the current batsman from the array
        let batsman = this.batsmen[this.currentBatterIndex];
        this.overHistory.push({
          out: true,
          teamid: batsman.teamid,
          match_id: Number(this.MatchId),
          id: batsman.id,
          name: batsman.name,
          runs: batsman.runs,
          value: 0,
          ballsFaced: batsman.ballsFaced,
          over: Math.floor(this.totalBallss() / 6) + 1,
          balltype: "NM",
          ballNumber: this.totalBallsInOverHistory() + 1,
        });
        const object = this.playerlist.pop();
        try {
          const player = {
            id: object.player_id,
            name: object.name,
            teamid: this.id,
            runs: 0,
            ballsFaced: 0,
            ballType: "NM",
          };
          this.batsmen.splice(this.currentBatterIndex, 1, player);
        } catch (error) {
          this.handleMatchOver();
        }
      }
    },
    handleMatchOver() {
      this.matchScoring();
      if (this.inning == 2) {
        this.handleMatchOverInning2();
      } else {
        this.handleMatchOverNextInning();
      }
    },

    handleMatchOverInning2() {
      Swal.fire({
        icon: "info",
        title: "Match over",
        showConfirmButton: true,
      }).then(() => {
        this.$router.push({
          name: "match-list",
          params: {
            TournamentId: this.$route?.params?.tournamentId,
          },
        }); // Redirect to the match-list page
      });
    },

    handleMatchOverNextInning() {
      Swal.fire({
        icon: "success",
        title: "match over, no more players ",
        text: "Let's start the next innings",
        showConfirmButton: true,
      }).then((result) => {
        this.batsmen = [];
        this.completedOvers = [];
        this.overHistory = [];
        this.bowlerlist = [];

        if (result.isConfirmed) {
          this.inning++;
          this.loadBowlerListAndPlayerList();
        }
      });
    },

    loadBowlerListAndPlayerList() {
      playerList(this.id).then(
        (response) => {
          this.bowlerlist = response.data;
          this.length = response.data.length;
        },
        (error) => {
          const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Oops.. Some unknown error occurred..!";
          this.$toast.show(errorMessage, {
            type: "error",
          });
        }
      );
      this.id = this.nonSelectedId;
      const selectedId = this.nonSelectedId;
      playerList(Number(selectedId)).then(
        (response) => {
          this.playerlist = response.data;
          this.length = response.data.length;
          if (this.length > 0) {
            this.batsmen = [];
            this.player1 = this.playerlist.pop();
            this.batsmen.push({
              match_id: Number(this.MatchId),
              teamid: selectedId,
              id: this.player1.player_id,
              name: this.player1.name,
              runs: 0,
              ballsFaced: 0,
              current: false,
            });
            this.player2 = this.playerlist.pop();
            this.batsmen.push({
              match_id: Number(this.MatchId),
              teamid: selectedId,
              id: this.player2.player_id,
              name: this.player2.name,
              runs: 0,
              ballsFaced: 0,
              current: false,
            });
          }
        },
        (error) => {
          const errorMessage =
            errorCodes[error.response.data.error_code] ||
            "Error generating a new player list.";
          this.$toast.show(errorMessage, {
            type: "error",
          });
        }
      );
    },

    undoLastBall() {
      if (this.overHistory.length > 0) {
        const lastBallData = this.overHistory.pop();
        const lastBallBatter = this.batsmen.find(
          (batsman) => batsman.name === lastBallData.name
        );
        let index;
        switch (true) {
          case lastBallData.value % 2 !== 0 && !lastBallData.out:
            this.swapBatsmen();
            if (lastBallBatter.runs >= lastBallData.value) {
              lastBallBatter.runs -= lastBallData.value;
            } else {
              lastBallBatter.runs = 0;
            }
            lastBallBatter.ballsFaced--;
            break;

          case lastBallData.out:
            this.playerlist.push({
              player_id: this.batsmen[this.currentBatterIndex].id,
              name: this.batsmen[this.currentBatterIndex].name,
              runs: this.batsmen[this.currentBatterIndex].runs,
              ballsFaced: this.batsmen[this.currentBatterIndex].ballsFaced,
            });
            this.batsmen.splice(this.currentBatterIndex, 1, {
              name: lastBallData.name,
              runs: lastBallData.runs,
              ballsFaced: lastBallData.ballsFaced,
              teamid: lastBallData.teamid,
              id: lastBallData.id,
            });

            index = this.batsmen.findIndex(
              (batsman) => batsman.name === lastBallData.name
            );
            this.currentBatterIndex = index;

            break;

          default:
            if (lastBallBatter.runs >= lastBallData.value) {
              lastBallBatter.runs -= lastBallData.value;
            } else {
              lastBallBatter.runs = 0;
            }
            lastBallBatter.ballsFaced--;
            break;
        }
      }
    },
    totalBallss() {
      const totalBallsInOverHistory = this.overHistory.reduce((overTotal) => {
        return overTotal + 1;
      }, 0);
      const totalBallsInCompletedOvers = this.completedOvers
        .flat()
        .reduce((completedOversTotal) => {
          return completedOversTotal + 1;
        }, 0);
      return totalBallsInOverHistory + totalBallsInCompletedOvers;
    },

    totalBallsInOverHistory() {
      return this.overHistory.reduce((Overhistorytotal) => {
        return Overhistorytotal + 1;
      }, 0);
    },

    async extraScore(runsByStriker, extras) {
      const isValid = await this.v$.$validate();
      if (isValid) {
        if (this.extraScoreStatus === "LB") {
          this.legByScore(extras);
        } else if (this.extraScoreStatus === "NB") {
          this.wideNoBallScore(runsByStriker, extras, "NB");
        } else {
          this.wideNoBallScore(runsByStriker, extras, "WD");
        }
      }
    },
    legByScore(extras) {
      const currentBatter = this.batsmen[this.currentBatterIndex]; //finding the current batter
      currentBatter.ballsFaced++;
      //adding 1 ball to the current batters balls faced
      this.overHistory.push({
        teamid: currentBatter.teamid,
        match_id: Number(this.MatchId),
        id: currentBatter.id,
        name: currentBatter.name,
        runs: currentBatter.runs,
        value: parseInt(extras, 10),
        ballsFaced: currentBatter.ballsFaced,
        over: Math.floor(this.totalBallss() / 6) + 1,
        balltype: "LB",
        ballNumber: this.totalBallsInOverHistory() + 1,
      });
      if (extras % 2 != 0) {
        //if the extra run is an odd number performs batsman swaping(in case of LB only extra run is there)
        this.swapBatsmen();
      }
      this.closeModal();
    },
    wideNoBallScore(runsByStriker, extras, name) {
      const currentBatter = this.batsmen[this.currentBatterIndex];
      currentBatter.runs += +runsByStriker;
      currentBatter.ballsFaced++;
      this.overHistory.push({
        teamid: currentBatter.teamid,
        match_id: Number(this.MatchId),
        id: currentBatter.id,
        name: currentBatter.name,
        runs: currentBatter.runs,
        value: +runsByStriker + extras,
        ballsFaced: currentBatter.ballsFaced,
        over: Math.floor(this.totalBallss() / 6) + 1,
        balltype: name,
        ballNumber: this.totalBallsInOverHistory() + 1,
      });
      if (runsByStriker % 2 != 0) {
        this.swapBatsmen();
      }
      this.extrasArray.push(extras);
      this.closeModal();
    },
    openModal(button) {
      this.selectedButton = button; // Save the clicked button value
      this.modalOpen = true;
      if (button === "LB") {
        this.runsByStriker = 0;
        this.extraScoreStatus = "LB";
        this.legByFlag = true;
        this.wideNoBallFlag = false;
      } else if (button === "NB") {
        this.legByFlag = false;
        this.wideNoBallFlag = true;
        this.runsByStriker = ""; // Set runsByStriker to an empty string for other cases
        this.extras = 1; // Set runsByStriker to an empty string for other cases
        this.extraScoreStatus = "NB";
      } else {
        this.runsByStriker = "";
        this.extras = 1; // Set runsByStriker to an empty string for other cases
        this.extraScoreStatus = "WD";
        this.legByFlag = false;
        this.wideNoBallFlag = true;
      }
    },
    closeModal() {
      this.modalOpen = false;
      this.extras = "";
      this.runsByStriker = "";
      this.extraScoreStatus = "";
      this.v$.$reset();
    },
  },
};
</script>
<style scoped>

/* Styles for the ball icon */

.info-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f0f0f0;
}
.batsman-info,
.bowler-info {
  text-align: center;
  color: rgb(27, 28, 118); /* Change this to the desired highlight color */
  font-weight: bold; /* Optionally, you can change the font weight to make it more noticeable */
  /* Add any other styles you want to apply to the highlighted batsman-info section */
}
.bowler-info p {
  margin: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .calculator-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .btn-square {
    width: 90px;
    height: 90px;
  }
  .info-box {
    flex-direction: column;
  }
}
.calculator-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 12px; /* Adjust the grid-row-gap value to reduce vertical space between buttons */
  /* Adjust the grid-column-gap value to reduce horizontal space between buttons */
  justify-content: center;
}

/* Adjust button width */
.btn-square {
  /* width: 200px; */
  height: 60px; /* Adjust the height to your desired size */
}
.overlay {
  position: relative;
}
.overlay::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.overlay-text {
  position: relative;
  color: white;
  z-index: 2;
}

.img-card {
  width: 100%;
  height: 250px;
  border-top-left-radius: 2px;
  border-top-right-radius: 2px;
  display: block;
  overflow: hidden;
}
.img-card img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  transition: all 0.25s ease;
}


.container {
  max-width: 1230px;
  width: 100%;
}



.form-wrap {
  background: rgba(255, 255, 255, 1);
  width: 100%;
  max-width: 2550px;
  padding: 50px;
  margin: 0 auto;
  position: relative;
  -webkit-border-radius: 10px;
  -moz-border-radius: 10px;
  border-radius: 10px;
  -webkit-box-shadow: 0px 0px 40px rgba(0, 0, 0, 0.15);
  -moz-box-shadow: 0px 0px 40px rgba(0, 0, 0, 0.15);
  box-shadow: 0px 0px 40px rgba(0, 0, 0, 0.15);
}
.modalContent {
  max-width: 300px;
  margin-left: 40%;
}
</style>
