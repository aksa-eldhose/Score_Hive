import { mount } from '@vue/test-utils';
import modal from '@/components/ModalComponent.vue';

describe('Modal Component Component', () => {
  it('renders the component correctly', () => {
      const wrapper = mount(modal);
      expect(wrapper.exists()).toBe(true);
    });
});