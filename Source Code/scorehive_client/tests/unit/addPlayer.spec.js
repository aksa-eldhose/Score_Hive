import { mount } from '@vue/test-utils';
import AddPlayer from '@/views/AddPlayer.vue';
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {  path: "/:pathMatch(.*)",
  name: "NotFound",
  component: () =>
    import(/* webpackChunkName: "createteam" */ "../views/NotFound.vue"),
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
  const mockRoute = {
    query: {
      team: 'MzB0b3VybmFtZW50Um91bmRz'
    },
  };
  describe('Add Player Component', () => {
    it('renders the component correctly', async () => {
      const mockT = (key) => key;
      const wrapper = mount(AddPlayer, {
        global: {
          mocks: {
            $route: mockRoute,
            $t: mockT
          },
        },
      });
        expect(wrapper.exists()).toBe(true);
      });
    });