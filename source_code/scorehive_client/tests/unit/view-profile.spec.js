import { mount } from '@vue/test-utils';
import viewProfile from '@/views/ViewProfile.vue';

describe('View Profile Component', () => {
    it('renders the component', () => {
    const mockT = (key) => key;
    const wrapper = mount(viewProfile, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
        expect(wrapper.exists()).toBe(true);
      });
    });