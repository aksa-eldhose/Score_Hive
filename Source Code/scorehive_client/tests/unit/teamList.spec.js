import { mount } from '@vue/test-utils';
import teamList from '@/views/TeamList.vue';

describe('Team List Component', () => {
    it('renders the component correctly', () => {
        const wrapper = mount(teamList);
        expect(wrapper.exists()).toBe(true);
      });
    });