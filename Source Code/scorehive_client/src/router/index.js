import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ListAllTournaments from "../views/ListAllTournaments.vue";
import TournamentDetail from "../views/TournamentDetail.vue";

const routes = [
  {
    path: "/",
    redirect: "/sign-in",
  },
  {
    path: "/home", //homepage
    name: "Home",
    pathMatch: "full",
    component: HomeView,
    meta: { requiresAuth: true },
  },
  {
    path: "/ListAllTournaments",
    name: "ListAllTournaments",
    pathMatch: "full",
    component: ListAllTournaments,
    meta: { requiresAuth: true },
  },

  {
    path: "/NavBar", //navbar
    name: "NavBar",
    pathMatch: "full",
    component: () => import("../views/NavBar.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/sign-in", //login
    name: "SignIn",
    pathMatch: "full",
    component: () => import("../views/SignIn.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/about",
    name: "about",
    meta: { requiresAuth: true },
    pathMatch: "full",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/sign-up", //verified user signup page
    name: "sign-up",
    pathMatch: "full",
    component: () => import("../views/SignUp.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/register-email", //email verification page for user registration
    name: "register-email",
    pathMatch: "full",
    component: () => import("../views/RegisterEmail.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/register-email-response/:id", //response for the email verification for user registration
    name: "register-email-response",
    pathMatch: "full",
    component: () => import("../views/RegisterEmailResponse.vue"),
  },
  {
    path: "/verify_ResetPassword/:id/:token",
    name: "verify_ResetPassword",
    pathMatch: "full",
    component: () => import("../views/VerifyResetPassword.vue"),
    meta: { requiresGuest: true },
  },

  {
    path: "/ResetPassword",
    name: "ResetPassword",
    pathMatch: "full",
    component: () =>
      import(
        /* webpackChunkName: "ResetPassword" */ "../views/ResetPassword.vue"
      ),
    meta: { requiresGuest: true },
  },
  {
    path: "/team-list/:teamId/player-list",
    name: "player-list",
    pathMatch: "full",
    component: () =>
      import(/* webpackChunkName: "PlayerList" */ "../views/PlayerList.vue"),
    meta: { requiresAuth: true },
  },

  {
    path: "/Joinedteam-list/:teamId/Joined-player-list",
    name: "Joined-player-list",
    pathMatch: "full",
    component: () =>
      import(
        /* webpackChunkName: "PlayerList" */ "../views/JoinedTeamplayers.vue"
      ),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournament-list", //listing team details
    name: "tournament-list",
    pathMatch: "full",
    component: () =>
      import(/* webpackChunkName: "team-list" */ "../views/TournamentList.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/ChangePassword",
    name: "ChangePassword",
    pathMatch: "full",
    component: () =>
      import(
        /* webpackChunkName: "createteam" */ "../views/ChangePassword.vue"
      ),
    meta: { requiresAuth: true },
  },
  {
    path: "/SendEmailResetPassword",
    name: "SendEmailResetPassword",
    pathMatch: "full",
    component: () =>
      import(
        /* webpackChunkName: "SendEmailResetPassword" */ "../views/SendEmailResetPassword.vue"
      ),
    meta: { requiresGuest: true },
  },
  {
    path: "/team-list", //listing team details
    name: "team-list",
    pathMatch: "full",
    component: () =>
      import(/* webpackChunkName: "team-list" */ "../views/TeamList.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/create-team",
    name: "CreateTeam",
    pathMatch: "full",
    component: () =>
      import(/* webpackChunkName: "createteam" */ "../views/CreateTeam.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/add-tournament",
    name: "add-tournament",
    pathMatch: "full",
    component: () =>
      import(/* webpackChunkName: "createteam" */ "../views/AddTournament.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/update-tournament",
    name: "update-tournament",
    pathMatch: "full",
    component: () =>
      import(
        /* webpackChunkName: "createteam" */ "../views/UpdateTournament.vue"
      ),
    meta: { requiresAuth: true },
  },
  {
    path: "/error",
    name: "error",
    pathMatch: "full",
    component: () =>
      import(/* webpackChunkName: "createteam" */ "../views/ErrorComponent.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/view-profile", //user profile details
    name: "View-profile",
    pathMatch: "full",
    component: () =>
      import(
        /* webpackChunkName: "View-profile" */ "../views/ViewProfile.vue"
      ),
    meta: { requiresAuth: true },
  },
  {
    path: "/profile-edit", //user profile edit
    name: "profile-edit",
    pathMatch: "full",
    component: () =>
      import(
        /* webpackChunkName: "profile-edit" */ "../views/ProfileEdit.vue"
      ),
    meta: { requiresAuth: true },
  },
  {
    path: "/add-player",
    name: "AddPlayer",
    pathMatch: "full",
    component: () =>
      import(/* webpackChunkName: "createteam" */ "../views/AddPlayer.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/update-team",
    name: "UpdateTeam",
    pathMatch: "full",
    component: () =>
      import(/* webpackChunkName: "updateteam" */ "../views/UpdateTeam.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/join-team",
    name: "JoinTeam",
    pathMatch: "full",
    component: () => import("../views/JoinTeam.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:TournamentId/teams",
    name: "tournament-teams",
    pathMatch: "full",
    component: () => import("../views/TournamentTeamsList.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:TournamentId/add-group",
    name: "add-group",
    pathMatch: "full",
    component: () => import("../views/AddGroup.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:TournamentId/groups",
    name: "group",
    pathMatch: "full",
    component: () => import("../views/GroupList.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:TournamentId/schedule-match",
    name: "schedule-match",
    pathMatch: "full",
    component: () => import("../views/AddMatch.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:TournamentId/update-match",
    name: "Update-match",
    pathMatch: "full",
    component: () => import("../views/UpdateMatch.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:TournamentId/add-rounds",
    name: "add-rounds",
    pathMatch: "full",
    component: () => import("../views/AddRounds.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:TournamentId/list-rounds",
    name: "list-rounds",
    pathMatch: "full",
    component: () => import("../views/RoundList.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournament/:TournamentId/:groupid/update-group",
    name: "update-group",
    pathMatch: "full",
    component: () => import("../views/UpdateGroup.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/match-list/:MatchId/:tournamentId/:team1/:team2/:id1/:id2/match-toss",
    name: "match-toss",
    pathMatch: "full",
    component: () => import("../views/MatchToss.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:TournamentId/match-list",
    name: "match-list",
    pathMatch: "full",
    component: () => import("../views/MatchList.vue"),
    meta: { requiresAuth: true },
  }, 
   {
    path: "/tournaments/match-list/:MatchId/:tournamentId/:team/:category/:id/:nonSelectedId/:nonSelectedTeam/match-scoring",
    name: "match-scoring",
    pathMatch: "full",
    component: () => import("../views/MatchScoring.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/match-details",
    name: "match-details",
    pathMatch: "full",
    component: () => import("../views/MatchDetails.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/TournamentDetail",
    name: "TournamentDetail",
    pathMatch: "full",
    component: TournamentDetail,
    meta: { requiresAuth: true },
    children: [
      {
        path: "AboutTournament",
        name: "AboutTournament",
        pathMatch: "full",
        component: () => import("../views/AboutTournament.vue"),
        // props: (route) => ({ tournamentId: route.query.tournamentId }),
        meta: { requiresAuth: true },
      },
      {
        path: "Match",
        name: "Match",
        pathMatch: "full",
        component: () => import("../views/TournamentMatch.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "PointTable",
        name: "PointTable",
        pathMatch: "full",
        component: () => import("../views/PointTable.vue"),
        meta: { requiresAuth: true },
      },
      {
        path: "TournamentTeam",
        name: "TournamentTeam",
        pathMatch: "full",
        component: () => import("../views/TournamentTeam.vue"),
        meta: { requiresAuth: true },
      },
     
    ],
  },
  {
    path: "/:pathMatch(.*)",
    name: "NotFound",
    component: () =>
      import(/* webpackChunkName: "createteam" */ "../views/NotFound.vue"),
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("Access_Token");
  if (to.matched.some((record) => record.meta.requiresGuest)) {
    if (!isAuthenticated) {
      next();
    } else {
      next("/home");
    }
  } else if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (isAuthenticated) {
      next();
    } else {
      next("/sign-in");
      window.history.replaceState(null, "", "/sign-in");
    }
  } else {
    next();
  }
});

export default router;
