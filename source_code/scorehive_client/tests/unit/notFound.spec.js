import { mount } from '@vue/test-utils';
import notFound from '@/views/NotFound.vue';

describe('MatchToss Component', () => {
  it('renders the component correctly', () => {
      const wrapper = mount(notFound);
      expect(wrapper.exists()).toBe(true);
    });
});