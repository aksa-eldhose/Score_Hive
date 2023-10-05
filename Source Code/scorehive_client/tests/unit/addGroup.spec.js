import { mount } from '@vue/test-utils';
import AddGroup from '@/views/AddGroup.vue';
import image from '@/assets/img/logos/tst-logo.jpg';
import noImage from '@/assets/img/logos/noImage.png';
import listEmpty from '@/assets/img/logos/EmptyFile.png';
describe('AddGroup', () => {
  const mockT = (key) => key; 
    const wrapper = mount(AddGroup, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
  it('renders the component', () => {
    expect(wrapper.exists()).toBe(true);
  });
  it('initializes with default data', () => {
    expect(wrapper.vm.teams).toEqual([]);
    expect(wrapper.vm.selectedTeams).toEqual([]);
    expect(wrapper.vm.image).toEqual(image);
    expect(wrapper.vm.noImage).toEqual(noImage);
    expect(wrapper.vm.name).toEqual('');
    expect(wrapper.vm.isLoading).toBe(false);
    expect(wrapper.vm.tournamentId).toEqual('');
    expect(wrapper.vm.listEmpty).toEqual(listEmpty);
    expect(wrapper.vm.flag).toBe(2);
  });
  it('displays the "Add_new_group" title', () => {
    const title = wrapper.find('h2');
    expect(title.text()).toBe('Add_new_group');
  });
  it('initial value of flag is 2', () => {
    expect(wrapper.vm.flag).toBe(2);
  });
  it('displays error message when no teams are available for grouping', async () => {
    // Set teams to an empty array
    wrapper.setData({ teams: [] });
  
    // Wait for the next tick to allow reactivity to update the DOM
    await wrapper.vm.$nextTick();
  
    // Check if the error message and button are displayed
    const errorMessage = wrapper.find('.text-danger');
    const submitButton = wrapper.find('.m-1:nth-child(1)'); // Adjust the selector to target the submit button
  
    expect(errorMessage.exists()).toBe(true);
    expect(submitButton.exists()).toBe(true); 
    expect(submitButton.text()).toBe('Submit'); 
  });
  
  it('enables submit button when form is valid', async () => {
    // Set form values to valid values
    wrapper.setData({
      name: 'Group 1',
      selectedTeams: [1, 2, 3],
    });

    // Wait for the next tick to allow reactivity to update the DOM
    await wrapper.vm.$nextTick();

    // Check if the submit button is enabled
    const submitButton = wrapper.find('.m-1');
    expect(submitButton.attributes('disabled')).toBeFalsy();
  });
 
});
