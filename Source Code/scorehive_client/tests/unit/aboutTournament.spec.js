import { mount } from '@vue/test-utils';
import aboutTournament from '@/views/AboutTournament.vue';
  const mockRoute = {
    query: {
      tournamentId: 'MzBUb3VybmFtZW50'
    },
  };
  
  describe('About Tournament Component', () => {
    it('renders the component correctly', async () => {
      const wrapper = mount(aboutTournament, {
        global: {
          mocks: {
            $route: mockRoute,
          },
        },
      });
      expect(wrapper.exists()).toBe(true);
});
});