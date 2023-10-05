import { mount } from '@vue/test-utils';
import layout from '@/components/Layout.vue';

describe('Layout Component Component', () => {
  it('renders the component correctly', () => {
      const wrapper = mount(layout);
      expect(wrapper.exists()).toBe(true);
    });
});