import { mount } from '@vue/test-utils';
import EditProfile from '@/views/ProfileEdit.vue';

describe('EditProfile', () => {
  it('renders the component correctly', async () => {
    const mockRoute = {
      name: 'View-profile'
    };

    const wrapper = mount(EditProfile, {
      global: {
        mocks: {
          $route: mockRoute
        }
      }
    });
    await wrapper.setData({
      name: 'John Doe',
      phone: '+91 9876543210'
    });

    // Trigger the submit method
    await wrapper.vm.submit();
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.$route.name).toBe('View-profile');
    wrapper.unmount();
  });
});

