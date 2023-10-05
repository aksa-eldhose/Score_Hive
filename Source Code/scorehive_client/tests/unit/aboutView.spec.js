import { mount } from '@vue/test-utils';
import AboutView from '@/views/AboutView.vue';

describe('About View Component', () => {
    it('renders the component', () => {
    const mockT = (key) => key;
    const wrapper = mount(AboutView, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
        expect(wrapper.exists()).toBe(true);
      });
    });