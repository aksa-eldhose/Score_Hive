import { mount } from '@vue/test-utils';
import UpdateTeam from '@/views/UpdateTeam.vue';

describe('Update Team Component', () => {
  it('renders the component correctly', () => {
    const mockRoute = {
      query: {
        teamId: '100'
      },
    };

    const wrapper = mount(UpdateTeam, {
      global: {
        mocks: {
          $route: mockRoute,
        },
      },
    });

    expect(wrapper.exists()).toBe(true);
  });
});
