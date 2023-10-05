import { mount } from '@vue/test-utils';
import alert from '@/components/AlertComponent.vue';

describe('Alert Component Component', () => {
  it('renders the component correctly', () => {
      const wrapper = mount(alert);
      expect(wrapper.exists()).toBe(true);
    });
});