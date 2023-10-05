import { shallowMount } from '@vue/test-utils';
import RegisterEmailResponse from '@/views/RegisterEmailResponse.vue';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {  path: "/sign-up", //verified user signup page
  name: "sign-up",
  pathMatch: "full",
  component: () => import("../views/SignUp.vue"),
  meta: { requiresGuest: true },
 },
  { path: "/home", //homepage
  name: "Home",
  pathMatch: "full",
  component: () => import("../views/HomeView.vue"),
  meta: { requiresAuth: true }, },
  {
    path: "/register-email", //email verification page for user registration
    name: "register-email",
    pathMatch: "full",
    component: () => import("../views/RegisterEmail.vue"),
    meta: { requiresGuest: true },
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Mocking Swal
const Swal = require('sweetalert2');
jest.mock('sweetalert2', () => ({
  fire: jest.fn(),
}));

const mockRoute = {
  params: {
    id: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imxha3NobWkubW9oYW4rMTlAaW5ub3ZhdHVyZWxhYnMuY29tIiwiZXhwIjoxNjk0NzY5NDY0LCJpYXQiOjE2OTQ3Njg1NjQsInB1cnBvc2UiOiJlbWFpbF92ZXJpZmljYXRpb25fdG9rZW4ifQ.t-3i6gQDyZEfxxsl2Xu_McafNqzmMKFQ_weFdE8-qCY'
  },
};

describe('Register email response', () => {
  it('renders the component correctly', async () => {
    const wrapper = shallowMount(RegisterEmailResponse, {
      global: {
        plugins: [router],
        mocks: {
          $route: mockRoute,
        },
      },
    });
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    wrapper.unmount();
  });
});
