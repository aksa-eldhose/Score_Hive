import { mount } from '@vue/test-utils';
import signIn from '@/views/SignIn.vue';

describe('SignIn Component', () => {
    it('renders the component', () => {
    const mockT = (key) => key;
    const wrapper = mount(signIn, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
        expect(wrapper.exists()).toBe(true);
      });
    });