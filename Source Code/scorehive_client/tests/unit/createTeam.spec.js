import { mount } from '@vue/test-utils';
import createTeam from '@/views/CreateTeam.vue';

describe('Create Team Component', () => {
    it('renders the component', () => {
    const mockT = (key) => key;
    const wrapper = mount(createTeam, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
        expect(wrapper.exists()).toBe(true);
      });
    });