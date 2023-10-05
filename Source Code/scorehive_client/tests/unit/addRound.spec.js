import { mount } from '@vue/test-utils';
import AddRound from '@/views/AddRounds.vue';

describe('Add Round Component', () => {
 
// Mocking Swal
const Swal = require('sweetalert2');
jest.mock('sweetalert2', () => ({
  fire: jest.fn(),
}));

const mockRoute = {
  params: {
    TournamentId: 'MzB0b3VybmFtZW50Um91bmRz'
  },
};
  it('renders the component correctly', async () => {
    const mockT = (key) => key;
    const wrapper = mount(AddRound, {
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