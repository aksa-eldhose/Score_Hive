import { mount } from '@vue/test-utils';
import MatchList from '@/views/TournamentMatch.vue'

describe('MatchList.vue', () => {
    it('renders shows the cards correctly', () => {
        const mockT = (key) => key; 
        const wrapper = mount(MatchList, {
          global: {
            mocks: {
              $t: mockT,
              $route: {
                query: {
                  tournamentId: 'MjhUb3VybmFtZW50'
                }
              },
            },
          },
        });
      const matchCards = wrapper.findAll('.card');
      expect(matchCards.length).toBe(wrapper.vm.matchList.length);
      const firstMatchTournament = wrapper.vm.matchList[0].tournament_name;
      const firstMatchCard = matchCards[0].find('.card-header');
      expect(firstMatchCard.text()).toContain(firstMatchTournament);

      const secondMatchTournament = wrapper.vm.matchList[1].tournament_name;
      const secondMatchCard = matchCards[1].find('.card-header');
      expect(secondMatchCard.text()).toContain(secondMatchTournament);

      const thirdMatchTournament = wrapper.vm.matchList[2].tournament_name;
      const thirdMatchCard = matchCards[2].find('.card-header');
      expect(thirdMatchCard.text()).toContain(thirdMatchTournament);

      const forthMatchTournament = wrapper.vm.matchList[3].tournament_name;
      const forthMatchCard = matchCards[3].find('.card-header');
      expect(forthMatchCard.text()).toContain(forthMatchTournament);

      const fifthMatchTournament = wrapper.vm.matchList[4].tournament_name;
      const fifthMatchCard = matchCards[4].find('.card-header');
      expect(fifthMatchCard.text()).toContain(fifthMatchTournament);

      const sixthMatchTournament = wrapper.vm.matchList[5].tournament_name;
      const sixthMatchCard = matchCards[5].find('.card-header');
      expect(sixthMatchCard.text()).toContain(sixthMatchTournament);
    });
  });
  
