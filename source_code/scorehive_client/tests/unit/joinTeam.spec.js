import { mount } from '@vue/test-utils';
import JoinTeam from '@/views/JoinTeam.vue';

describe('JoinTeam Component', () => {
  it('renders the component correctly', () => {
      const wrapper = mount(JoinTeam);
      expect(wrapper.exists()).toBe(true);
    });
});