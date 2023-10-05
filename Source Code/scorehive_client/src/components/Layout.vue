<template>
    <nav class="navbar">
        <!-- LOGO -->
        <div class="logo">
            <RouterLink :to="{ name: 'SignIn' }" class="text-sm ml-2 mr-2 hover:text-blue-500 cursor-pointer">
                <img style="width: 200px" src="logo_6.png" alt="Image" />
            </RouterLink>
        </div>

        <!-- NAVIGATION MENU -->
        <ul class="nav-links">

            <!-- USING CHECKBOX HACK -->
            <input type="checkbox" id="checkbox_toggle" />
            <label for="checkbox_toggle" class="hamburger">&#9776;</label>
            <!-- NAVIGATION MENUS -->
            <div class="menu">
                <li><a href="/home">LIVE SCORES</a></li>
                <li><a href="/home">NETWORK</a></li>
                <li><a href="/home">SERVICES</a></li>
                <li class="services">
                    <em class="fa fa-people"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                            fill="currentColor" class="bi bi-person" viewBox="0 0 16 16">
                            <path
                                d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4Zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10Z" />
                        </svg> Profile</em>
                    <!-- Dropdown menu -->
                    <ul class="dropdown">
                        <h6 class="text-center"></h6>
                        <hr>
                        <li><a href="/editprofile">Edit Profile</a>
                        </li>
                        <li><a href="/ChangePassword">Change password</a>
                        </li>
                        <hr>
                        <li><a href="/">My Matches</a></li>
                        <li><a href="/">My Tournaments</a></li>
                        <li><a href="/">My Teams</a></li>
                        <li><a href="/">Organiser Admin</a></li>
                        <li><a href="/" @click="logout()">Log Out</a></li>
                    </ul>
                </li>
                <li>
                 <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                        class="bi bi-search" viewBox="0 0 16 16">
                        <path
                            d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                    </svg>
                </li>
                <li></li>
              
                <li></li>

            </div>
        </ul>
    </nav>
    <router-view></router-view>

</template>
<style scoped>
* {
margin: 0;
padding: 0;
box-sizing: border-box;
}

body {
font-family: cursive;
}

a {
text-decoration: none;
}

li {
list-style: none;
}

/* NAVBAR STYLING STARTS */
.navbar {
display: flex;
align-items: center;
justify-content: space-between;
padding: 20px;
background-color: hsl(217, 33%, 33%);
color: #fff;
}

.nav-links a {
color: #fff;
}

/* LOGO */
.logo {
font-size: 32px;
}

/* NAVBAR MENU */
.menu {
display: flex;
gap: 1em;
font-size: 15px;
}

.menu li:hover {
background-color: hsl(218, 41%, 30%);
border-radius: 5px;
transition: 0.3s ease;
}

.menu li {
padding: 5px 14px;
}

/* DROPDOWN MENU */
.services {
position: relative;
}

.profile {
position: relative;
}

.dropdown {
background-color: hsl(218, 41%, 30%);
padding: 1em 0;
position: absolute;
/*WITH RESPECT TO PARENT*/
display: none;
border-radius: 8px;
top: 35px;

}

.dropdown li+li {
margin-top: 10px;
}

.dropdown li {
padding: 0.5em 1em;
width: 12em;
text-align: left;
}

.dropdown li:hover {
background-color: hsl(218, 21%, 53%)
}

.services:hover .dropdown {
display: block;
}

input[type=checkbox] {
display: none;
}

/* HAMBURGER MENU */
.hamburger {
display: none;
font-size: 24px;
user-select: none;
}

/* APPLYING MEDIA QUERIES */
@media (max-width: 768px) {
.menu {
    display: none;
    position: absolute;
    background-color: hsl(218, 41%, 30%);
    right: 0;
    left: 0;
    text-align: center;
    padding: 16px 0;
}

.menu li:hover {
    display: inline-block;
    background-color: hsl(218, 41%, 30%);
    border-radius: 5px;
    transition: 0.3s ease;
}

.menu li+li {
    margin-top: 12px;
}

input[type=checkbox]:checked~.menu {
    display: block;
}

.hamburger {
    display: block;
}

.dropdown {
    left: 50%;
    top: 30px;
    transform: translateX(35%);
}

.dropdown li:hover {
    background-color: hsl(218, 21%, 53%);
}
}
</style>
<script>
import { defineComponent } from 'vue';
export default defineComponent({
name: 'LayOut',

components: {
},
methods: {
    logout() {
        localStorage.clear()
        this.$router.push({ name: "SignIn" })
    }
}
});
</script>