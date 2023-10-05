import { mount } from '@vue/test-utils';
import MatchToss from '@/views/MatchToss.vue';

describe('MatchToss Component', () => {
  it('renders the component correctly', () => {
      const wrapper = mount(MatchToss);
      expect(wrapper.exists()).toBe(true);
    });
});