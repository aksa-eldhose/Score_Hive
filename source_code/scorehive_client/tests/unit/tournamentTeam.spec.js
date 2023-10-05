import { mount } from '@vue/test-utils';
import TournamentTeam from '@/views/TournamentTeam.vue';

describe('Tournament Team Component', () => {
  it('renders the component correctly', () => {
    const mockRoute = {
      query: {
        tournamentId: 'MzBUb3VybmFtZW50'
      },
    };
    const wrapper = mount(TournamentTeam, {
      global: {
        mocks: {
          $route: mockRoute,
        },
      },
    });

    expect(wrapper.exists()).toBe(true);
  });
    });