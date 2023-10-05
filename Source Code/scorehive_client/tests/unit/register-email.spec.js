import { shallowMount } from '@vue/test-utils';
import RegisterEmail from '@/views/RegisterEmail.vue';
describe('RegisterEmail', () => {
  it('renders the component correctly', () => {
    const wrapper = shallowMount(RegisterEmail);
    expect(wrapper.exists()).toBe(true);
  });
});
