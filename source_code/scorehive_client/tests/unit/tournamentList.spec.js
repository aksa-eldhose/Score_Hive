import { mount } from '@vue/test-utils';
import TournamentList from '@/views/TournamentList.vue';

describe('Team List Component', () => {
    it('renders the component correctly', () => {
        const wrapper = mount(TournamentList);
        expect(wrapper.exists()).toBe(true);
      });
    });
