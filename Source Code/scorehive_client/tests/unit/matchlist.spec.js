import { shallowMount } from '@vue/test-utils';
import matchList from '@/views/MatchList.vue';
import axios from 'axios';

describe('matchList', () => {
    it('renders correctly', () => {
        const wrapper = shallowMount(matchList);
        expect(wrapper.exists()).toBe(true);
    });
    it('fetches team list on component mount', async () => {
        // Mock the API call using axios
        const matchList = [
          { match_between: "Team A vs Team B", Ground:"Kochi",date:"2023-07-07" },
          { match_between: "Team A vs Team B", Ground:"Kochi",date:"2023-07-07" },
          { match_between: "Team A vs Team B", Ground:"Kochi",date:"2023-07-07" },
          { match_between: "Team A vs Team B", Ground:"Kochi",date:"2023-07-07" },
    
        ];
        jest.spyOn(axios, 'get').mockResolvedValue({ data: matchList });

        // Mount the component
        const wrapper = shallowMount(matchList);

        // Wait for the next tick using `await wrapper.vm.$nextTick()`
        await wrapper.vm.$nextTick();
    });
 
});