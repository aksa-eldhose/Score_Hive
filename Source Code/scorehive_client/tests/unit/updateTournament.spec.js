import { mount } from '@vue/test-utils';
import updateTournament from '@/views/UpdateTournament.vue';

describe('Update Tournament Component', () => {
  let wrapper;

  beforeEach(() => {
    const mockT = (key) => key;
     wrapper = mount(updateTournament, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
  });
    it('renders the component', () => {
        expect(wrapper.exists()).toBe(true);
      });
      it('updates tournament_name data when input value changes', async () => {
        const input = wrapper.find('#name');
    
        await input.setValue('New Tournament Name');
    
        expect(wrapper.vm.tournament_name).toBe('New Tournament Name');
      });
      it('displays an error message if start date is not selected', async () => {
        const form = wrapper.find('form');
    
        await form.trigger('submit.prevent');
    
        const errorMessage = wrapper.find('#startDateError');
        expect(errorMessage.exists()).toBe(true);
        expect(errorMessage.text()).toContain('Value is required');
      });
    });