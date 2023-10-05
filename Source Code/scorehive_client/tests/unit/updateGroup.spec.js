import { mount } from '@vue/test-utils';
import updateGroup from '@/views/UpdateGroup.vue';

describe('Update Group Component', () => {
    it('renders the component', () => {
    const mockT = (key) => key;
    const wrapper = mount(updateGroup, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
        expect(wrapper.exists()).toBe(true);
      });
    });