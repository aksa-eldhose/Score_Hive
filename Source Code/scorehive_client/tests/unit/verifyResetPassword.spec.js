import VerifyResetPassword from '@/views/VerifyResetPassword.vue';
import { shallowMount } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {  
    path: "/sign-in", //login
    name: "SignIn",
    pathMatch: "full",
    component: () => import("../views/SignIn.vue"),
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

describe('VerifyResetPassword', () => {
  it('renders the component correctly', async () => {
    const wrapper = shallowMount(VerifyResetPassword, {
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
