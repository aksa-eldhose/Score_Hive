import { mount } from '@vue/test-utils';
import error from '@/views/ErrorComponent.vue';

describe('error Component', () => {
  it('renders the component correctly', () => {
      const wrapper = mount(error);
      expect(wrapper.exists()).toBe(true);
    });

});