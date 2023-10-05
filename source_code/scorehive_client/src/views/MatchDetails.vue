<template>
  <NavBar />
  <div class="d-flex justify-content-center">
    <div class="card shadow-lg mx-lg-5 my-lg-5 bg-white p-4 w-100 h-200">
      <h2>Match Details</h2>
      <div class="row">
        <div class="col-md-12 py-3">
          <div class="card">
            <div class="row no-gutters">
              <div class="col-md-4">
                <!-- Add your image here -->
                <img
                  src="https://i.pinimg.com/736x/bc/39/66/bc3966c2fcc8760069f7dcdf44da097d.jpg"
                  class="card-img"
                  alt="Image"
                />
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <!-- Rest of your card content -->
                  <h5 class="card-title text-success">
                    Summer slam truly corporate-2023
                  </h5>
                  <p class="card-text text-info">
                    Mamchand Cricket Club, Sonipat, 20 Ov., Limited Overs,
                    20-Jul-23 08:17 PM
                  </p>
                  <p class="card-text">Toss: FIMS HOSPITAL opt to field</p>
                  <p class="card-text">SONIPAT WARRIORS</p>
                  <p class="card-text">FIMS HOSPITAL</p>
                  <p class="card-text">
                    Match Tied (FIMS HOSPITAL won the super over)
                  </p>
                  <div class="d-flex justify-content-start">
                    <div class="mr-2 px-2">
                      <a
                        data-testid="score-card-link"
                        href="#"
                        @click="showCard(1)"
                        class="mr-2"
                        :class="{ 'active-link': showNewCard === 1 }"
                        >Summary</a
                      >
                    </div>
                    <div class="mr-2 px-2">
                      <a
                        data-testid="score-card-link"
                        href="#"
                        @click="showCard(2)"
                        class="mr-2"
                        :class="{ 'active-link': showNewCard === 2}"
                        >Score Card</a
                      >
                    </div>
                    <div class="mr-2 px-2">
                      <a
                        data-testid="score-card-link"
                        href="#"
                        class="mr-2"
                        @click="showCard(3)"
                        :class="{ 'active-link': showNewCard === 3 }"
                        >Teams</a
                      >
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm-12 justify-content-center">
          <div class="card" v-if="showNewCard === 1">
            <div class="card-body">
              <div class="card-header py-4 bg-blue fs-4">Best Performances</div>
              <ul class="list-group list-group">
                <div class="card-header py-4 bg-light fs-8">Batters</div>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Cras justo odio</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">Runs: 32</span>
                    <span class="px-4 text-success">4s: 4</span>
                    <span class="px-4 text-success">6S: 3</span>
                    <span class="px-4 text-success">Balls: 7</span>
                    <span class="px-4 text-success">SR</span>
                  </div>
                </li>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Vestibulum at eros</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">Runs: 32</span>
                    <span class="px-4 text-success">4s: 4</span>
                    <span class="px-4 text-success">6S: 3</span>
                    <span class="px-4 text-success">Balls: 7</span>
                    <span class="px-4 text-success">SR</span>
                  </div>
                </li>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Dapibus ac facilisis in</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">Runs: 32</span>
                    <span class="px-4 text-success">4s: 4</span>
                    <span class="px-4 text-success">6S: 3</span>
                    <span class="px-4 text-success">Balls: 7</span>
                    <span class="px-4 text-success">SR</span>
                  </div>
                </li>
              </ul>
              <br />
              <ul class="list-group list-group">
                <div class="card-header py-4 bg-light fs-8">Bowlers</div>

                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Cras justo odio</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">O 1</span>
                    <span class="px-4 text-success">M: 4</span>
                    <span class="px-4 text-success">R: 3</span>
                    <span class="px-4 text-success">W: 7</span>
                    <span class="px-4 text-success">0S</span>
                    <span class="px-4 text-success">4S</span>
                    <span class="px-4 text-success">6S</span>
                    <span class="px-4 text-success">NB</span>
                    <span class="px-4 text-success">WD</span>
                  </div>
                </li>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Vestibulum at eros</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">O 1</span>
                    <span class="px-4 text-success">M: 4</span>
                    <span class="px-4 text-success">R: 3</span>
                    <span class="px-4 text-success">W: 7</span>
                    <span class="px-4 text-success">0S</span>
                    <span class="px-4 text-success">4S</span>
                    <span class="px-4 text-success">6S</span>
                    <span class="px-4 text-success">NB</span>
                    <span class="px-4 text-success">WD</span>
                  </div>
                </li>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Dapibus ac facilisis in</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">O 1</span>
                    <span class="px-4 text-success">M: 4</span>
                    <span class="px-4 text-success">R: 3</span>
                    <span class="px-4 text-success">W: 7</span>
                    <span class="px-4 text-success">0S</span>
                    <span class="px-4 text-success">4S</span>
                    <span class="px-4 text-success">6S</span>
                    <span class="px-4 text-success">NB</span>
                    <span class="px-4 text-success">WD</span>
                  </div>
                </li>
              </ul>
            </div>
          </div> <div class="card" v-if="showNewCard === 2">
            <div class="card-body">
              <div class="card-header py-4 bg-blue fs-4">Best Performances</div>
              <ul class="list-group list-group">
                <div class="card-header py-4 bg-light fs-8">Batters</div>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Cras justo odio</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">Runs: 32</span>
                    <span class="px-4 text-success">4s: 4</span>
                    <span class="px-4 text-success">6S: 3</span>
                    <span class="px-4 text-success">Balls: 7</span>
                    <span class="px-4 text-success">SR</span>
                  </div>
                </li>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Vestibulum at eros</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">Runs: 32</span>
                    <span class="px-4 text-success">4s: 4</span>
                    <span class="px-4 text-success">6S: 3</span>
                    <span class="px-4 text-success">Balls: 7</span>
                    <span class="px-4 text-success">SR</span>
                  </div>
                </li>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Dapibus ac facilisis in</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">Runs: 32</span>
                    <span class="px-4 text-success">4s: 4</span>
                    <span class="px-4 text-success">6S: 3</span>
                    <span class="px-4 text-success">Balls: 7</span>
                    <span class="px-4 text-success">SR</span>
                  </div>
                </li>
              </ul>
              <br />
              <ul class="list-group list-group">
                <div class="card-header py-4 bg-light fs-8">Bowlers</div>

                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Cras justo odio</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">O 1</span>
                    <span class="px-4 text-success">M: 4</span>
                    <span class="px-4 text-success">R: 3</span>
                    <span class="px-4 text-success">W: 7</span>
                    <span class="px-4 text-success">0S</span>
                    <span class="px-4 text-success">4S</span>
                    <span class="px-4 text-success">6S</span>
                    <span class="px-4 text-success">NB</span>
                    <span class="px-4 text-success">WD</span>
                  </div>
                </li>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Vestibulum at eros</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">O 1</span>
                    <span class="px-4 text-success">M: 4</span>
                    <span class="px-4 text-success">R: 3</span>
                    <span class="px-4 text-success">W: 7</span>
                    <span class="px-4 text-success">0S</span>
                    <span class="px-4 text-success">4S</span>
                    <span class="px-4 text-success">6S</span>
                    <span class="px-4 text-success">NB</span>
                    <span class="px-4 text-success">WD</span>
                  </div>
                </li>
                <li
                  class="list-group-item py-3 d-flex justify-content-between align-items-center"
                >
                  <span>Dapibus ac facilisis in</span>
                  <div class="ml-auto">
                    <span class="px-4 text-primary">O 1</span>
                    <span class="px-4 text-success">M: 4</span>
                    <span class="px-4 text-success">R: 3</span>
                    <span class="px-4 text-success">W: 7</span>
                    <span class="px-4 text-success">0S</span>
                    <span class="px-4 text-success">4S</span>
                    <span class="px-4 text-success">6S</span>
                    <span class="px-4 text-success">NB</span>
                    <span class="px-4 text-success">WD</span>
                  </div>
                </li>
              </ul>
            </div>
          </div>
          <div class="card" v-if="showNewCard === 3">
            <div class="container">
              <div class="row">
                <div class="d-flex align-items-center">
                  <a
                    class="img-card d-flex justify-content-center align-items-center"
                    style="width: 100px; height: 100px"
                  >
                    <img
                      class="rounded-circle"
                      :src="noImage"
                      alt=""
                      style="max-width: 50%; max-height: 50%"
                    />
                  </a>
                  <h6>Team CSK</h6>
                </div>
                <div
                  class="col-md-3"
                  v-for="player in teamA_Players"
                  :key="player.id"
                >
                  <div
                    class="card m-3 shadow"
                    style="max-width: 200px; max-height: 250px"
                  >
                    <a class="img-card">
                      <img
                        :src="user_profile"
                        alt=""
                        style="max-width: 199px; max-height: 200px"
                      />
                    </a>
                    <div class="card-content">
                      <div class="d-flex flex-wrap justify-content-center">
                        <p class="text-center mt-2">
                          {{ player.name }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="container">
              <div class="row">
                <div class="d-flex align-items-center">
                  <a
                    class="img-card d-flex justify-content-center align-items-center"
                    style="width: 100px; height: 100px"
                  >
                    <img
                      class="rounded-circle"
                      :src="noImage"
                      alt=""
                      style="max-width: 50%; max-height: 50%"
                    />
                  </a>
                  <h6>Team PTD</h6>
                </div>
                <div
                  class="col-md-3"
                  v-for="player in teamB_Players"
                  :key="player.id"
                >
                  <div
                    class="card m-3 shadow"
                    style="max-width: 200px; max-height: 240px"
                  >
                    <a class="img-card">
                      <img
                        :src="user_profile"
                        alt=""
                        style="max-width: 199px; max-height: 200px"
                      />
                    </a>
                    <div class="card-content">
                      <div class="d-flex flex-wrap justify-content-center">
                        <p class="text-center">
                          {{ player.name }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import NavBar from "./NavBar.vue";
import user_profile from "@/assets/img/user_profile.png";
import noImage from "@/assets/img/cric-2plrs.jpg";
export default {
  components: {
    NavBar,
  },
  data() {
    return {
      showNewCard: 1, // No card initially displayed
      user_profile,
      noImage,
      teamA_Players: [
        { id: "1", name: "Rahul" },
        { id: "2", name: "Rohit" },
        { id: "3", name: "Sameer" },
        { id: "4", name: "Mayank" },
        { id: "5", name: "Virat" },
        { id: "6", name: "Karan" },
        { id: "7", name: "Sidharth" },
        { id: "8", name: "Shlok" },
        { id: "9", name: "Prayank" },
        { id: "10", name: "Rishi" },
      ],
      teamB_Players: [
        { id: "1", name: "Aniketh" },
        { id: "2", name: "Veer" },
        { id: "3", name: "Jai" },
        { id: "4", name: "Mohith" },
        { id: "5", name: "Prem" },
        { id: "6", name: "Aswin" },
        { id: "7", name: "Karthik" },
        { id: "8", name: "Madhav" },
        { id: "9", name: "Anirudh" },
        { id: "10", name: "Akash" },
      ],
    };
  },
  methods: {
    showCard(cardNumber) {
      this.showNewCard = cardNumber; // Show the selected card
    },
  },
};
</script>
<style scoped>
.active-link {
  font-weight: bold; /* Increase the font weight to make it bold */
  color: #bf0e1d; /* Change the color to a highlight color */
  text-decoration: underline; /* Add an underline to the link */
}
</style>
