<template>
  <head>
  <title>NavBar</title>

    <meta charset="UTF-8" />
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
    />
  </head>
  <body>
    <nav>
      <div class="logo">
        <RouterLink
          :to="{ name: 'Home' }"
          class="text-sm ml-2 mr-2 hover:text-blue-500 cursor-pointer"
        >
          <img style="width: 200px" :src="scorehive" alt="Image" />
        </RouterLink>
      </div>
      <label for="btn" class="icon">
        <span class="fa fa-bars"></span>
      </label>
      <input type="checkbox" id="btn" />
      <ul>
        <li>
          <Router-link :to="{ name: 'ListAllTournaments' }"
            >TOURNAMENTS
          </Router-link>
        </li>
        <li>
          <label for="btn-2" class="show" id="services-item"
            ><a style="cursor: pointer" class="text-white"
              ><svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="white"
                class="bi bi-person"
                viewBox="0 0 16 16"
              >
                <path
                  d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"
                />
              </svg>
              PROFILE</a
            ></label
          >
          <a style="cursor: pointer" class="text-white"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="white"
              class="bi bi-person"
              viewBox="0 0 16 16"
            >
              <path
                d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z"
              />
            </svg>
            PROFILE</a
          >
          <input type="checkbox" id="btn-2" />
          <ul>
            <li>
              <Router-link :to="{ name: 'View-profile' }"
                >View Profile
              </Router-link>
            </li>

            <li><a href="/home">My Matches</a></li>
            <li><a href="/tournament-list">My Tournaments</a></li>
            <li>
              <Router-link :to="{ name: 'team-list' }">Teams</Router-link>
            </li>
            <li>
              <a
                class="text-white"
                style="cursor: pointer"
                @click.prevent="logout()"
                >Log Out</a
              >
            </li>
          </ul>
        </li>
      </ul>
    </nav>
  </body>
</template>
<style scoped>
@import url("https://fonts.googleapis.com/css?family=Poppins:400,500,600,700&display=swap");

* {
  margin: 0;
  padding: 0;
  user-select: none;
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
  font-size: 18px;
  /* overflow-y: hidden; */
}

nav {
  background: hsl(217, 33%, 33%);
  font-size: 18px;
}

nav:after {
  content: "";
  clear: both;
  display: table;
}

#services-item {
  height: 50px;
  font-size: 18px;
}

nav .logo {
  float: left;
  color: white;
  text-transform: uppercase;
  font-size: 25px;
  font-weight: 600;
  line-height: 70px;
  padding-left: 30px;
}

nav ul {
  float: right;
  margin-right: 50px;
  list-style: none;
  position: relative;
}

nav ul li {
  /* float: left; */
  display: inline-block;
  background: hsl(217, 33%, 33%);
  margin: 0 5px;
  z-index: 10;
}

nav ul li a {
  color: white;
  line-height: 70px;
  text-decoration: none;
  font-size: 12px;
  padding: 8px 15px;
  text-transform: uppercae;
  font-weight: 600;
}
nav ul a {
  color: white;
  line-height: 70px;
  text-decoration: none;
  font-size: 14px;
  padding: 8px 15px;
  text-transform: uppercae;
  font-weight: 600;
}
nav ul li a:hover {
  color: rgb(218, 206, 208);
}

nav ul ul {
  position: absolute;
  top: 90px;
  opacity: 0;
  visibility: hidden;
  transition: top 0.3s;
}

nav ul li:hover > ul {
  top: 70px;
  opacity: 1;
  visibility: visible;
}

nav ul ul li {
  position: relative;
  margin: 0px;
  width: 150px;
  float: none;
  display: list-item;
  border-bottom: 1px solid rgba(0, 0, 0, 0.3);
}

nav ul ul li a {
  line-height: 50px;
}

nav ul ul ul li {
  position: relative;
  top: -60px;
  left: 150px;
}

.show,
.icon,
input {
  display: none;
}

.fa-plus {
  font-size: 15px;
  margin-left: 40px;
}

@media all and (max-width: 968px) {
  nav ul {
    margin-right: 0px;
    float: left;
  }

  nav .logo {
    padding-left: 30px;
    width: 100%;
  }

  .show + a,
  ul {
    display: none;
  }

  nav ul li,
  nav ul ul li {
    display: block;
    width: 100%;
  }

  .show {
    display: block;
    color: white;
    font-size: 18px;
    text-transform: uppercase;
    padding: 0 20px;
    line-height: 70px;
    font-weight: 600;
    cursor: pointer;
  }

  .icon {
    display: block;
    color: white;
    position: absolute;
    top: 0;
    right: 40px;
    line-height: 70px;
    cursor: pointer;
    font-size: 25px;
  }

  nav ul ul {
    top: 70px;
    border-top: 0px;
    float: none;
    position: static;
    display: none;
    opacity: 1;
    visibility: visible;
  }

  nav ul ul a {
    padding-left: 40px;
  }

  nav ul ul ul a {
    padding-left: 80px;
  }

  nav ul ul ul li {
    position: static;
  }

  [id^="btn"]:checked + ul {
    display: block;
  }

  nav ul ul li {
    border-bottom: 0px;
  }
}
</style>

<script>
import cric from "@/assets/img/cric.png";
import scorehive from "@/assets/img/logo_6.png";
import { defineComponent } from "vue";
export default defineComponent({
  name: "NavBar",
  data() {
    return {
      cric: cric,
      scorehive: scorehive,
    };
  },
  components: {},
  methods: {
    logout() {
      localStorage.clear();
      window.history.go(0);
      this.$router.push({ name: "SignIn" });
    },
  },
});
</script>
