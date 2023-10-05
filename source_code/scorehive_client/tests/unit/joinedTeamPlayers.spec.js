import { mount } from '@vue/test-utils';
import joinedTeamPlayers from '@/views/JoinedTeamplayers.vue';

describe('Joined Team Players Component', () => {
    it('renders the component', () => {
      const mockRoute = {
        params: {
          teamId: 'ODhUZWFt'
        },
      };
    const mockT = (key) => key;
    const wrapper = mount(joinedTeamPlayers, {
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