import { shallowMount } from '@vue/test-utils';
import tournamnetTeams from '@/views/TournamentTeamsList.vue';

describe('Tournamnet Teams', () => {
   
  it('renders the component', () => {
    const mockT = (key) => key; 
    const wrapper = shallowMount(tournamnetTeams, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
    expect(wrapper.exists()).toBe(true);
  });
  it('displays the team name in the table', () => {
    const teamlist = [
      { id: 1, name: 'Team A' },
      { id: 2, name: 'Team B' },
      { id: 3, name: 'Team C' },
    ];
    const wrapper = shallowMount(tournamnetTeams, {
      data() {
        return {
          teamlist: teamlist,
        };
      },
    });

    const rows = wrapper.findAll('tbody tr');

    expect(rows.length).toBe(teamlist.length);

    for (let i = 0; i < teamlist.length; i++) {
      const row = rows[i];
      const teamName = teamlist[i].name;

      expect(row.text()).toContain(teamName);
    }
  });
  it('opens the modal when the add team button is clicked', async () => {
    const wrapper = shallowMount(tournamnetTeams);
    const addButton = wrapper.findComponent({ name: 'ButtonComponent' });

    expect(wrapper.vm.modalOpen).toBe(false);

    await addButton.trigger('click');

    expect(wrapper.vm.modalOpen).toBe(true);
  });
});
