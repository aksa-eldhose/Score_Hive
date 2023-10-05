import { mount } from '@vue/test-utils';
import AddTournament from '@/views/AddTournament.vue';

describe('Add Tournament Component', () => {
    it('renders the component', () => {
    const mockT = (key) => key;
    const wrapper = mount(AddTournament, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
        expect(wrapper.exists()).toBe(true);
      });
    });