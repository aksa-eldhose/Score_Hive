import { mount } from '@vue/test-utils';
import groupList from '@/views/GroupList.vue';

describe('groupList', () => {
  const mockT = (key) => key; 
      const wrapper = mount(groupList, {
          global: {
            mocks: {
              $t: mockT,
            },
          },
        });

  it('renders correctly', () => {
            expect(wrapper.exists()).toBe(true);
  });

  it('displays the "No_groups_are_added" message when the grouplist is empty', async () => {
    wrapper.setData({ grouplist: [] });
    await wrapper.vm.$nextTick();
    const message = wrapper.find('.text-center p');
    expect(message.text()).toBe('No_groups_are_added');
  });

  it('renders the table when the grouplist is not empty', async () => {
    wrapper.setData({
      grouplist: [
        { id: 1, name: 'Group 1', teams: [] },
        { id: 2, name: 'Group 2', teams: [] },
        { id: 3, name: 'Group 3', teams: [] },
        { id: 4, name: 'Group 4', teams: [] },
      ],
    });
    
    await wrapper.vm.$nextTick();
    const table = wrapper.find('table');
    expect(table.exists()).toBe(true);
    const rows = wrapper.findAll('.datas');
    expect(rows.length).toBe(4);
  });

  it('expands/collapses the row when the toggle icon is clicked', async () => {
    wrapper.setData({
      grouplist: [
        { id: 1, name: 'Group 1', teams: [] },
        { id: 2, name: 'Group 2', teams: [] },
      ],
    });
    await wrapper.vm.$nextTick();
    const toggleIcon = wrapper.find('.toggle-icon');
    toggleIcon.trigger('click');
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.expandedRows).toEqual([1]);
    toggleIcon.trigger('click');
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.expandedRows).toEqual([]);
  });

  it('calls the addGroup method when "Add group" button is clicked', async () => {
    const addGroupMock = jest.fn();
    wrapper.vm.addGroup = addGroupMock;
    await wrapper.vm.$nextTick();
  
    const addButton = wrapper.find('.h-25');
    addButton.trigger('click');
  
    expect(addGroupMock).toHaveBeenCalled();
  });
  
  it('disables the "Add group" button when isEnded is true', async () => {
    wrapper.setData({ isEnded: true });
    await wrapper.vm.$nextTick();
  
    const addButton = wrapper.find('.h-25');
    expect(addButton.element.disabled).toBeTruthy();
  });
});