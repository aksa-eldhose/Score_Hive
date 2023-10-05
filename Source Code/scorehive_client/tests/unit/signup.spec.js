import { mount } from '@vue/test-utils';
import SignUp from '@/views/SignUp.vue';

describe('SignUp Component', () => {
    it('renders the component', () => {
    const mockT = (key) => key;
    const wrapper = mount(SignUp, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
        expect(wrapper.exists()).toBe(true);
      });
      it('displays a sign-up form', () => {
        const mockT = (key) => key;
    const wrapper = mount(SignUp, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
        expect(wrapper.find('form').exists()).toBe(true);
      });

  it('updates the name data on input', async () => {
    const mockT = (key) => key;
    const wrapper = mount(SignUp, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
    await wrapper.find('input#floatingEmail').setValue('John Doe');
    expect(wrapper.vm.name).toBe('John Doe');
  });
  it('updates the phone data on input', async () => {
    const mockT = (key) => key;
    const wrapper = mount(SignUp, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
    await wrapper.find('input#floatingPhone').setValue('1234567890');
    expect(wrapper.vm.phone).toBe('1234567890');
  });
  it('updates the password data on input', async () => {
    const mockT = (key) => key;
    const wrapper = mount(SignUp, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
    await wrapper.find('input#floatingPassword').setValue('Password123');
    expect(wrapper.vm.password).toBe('Password123');
  });
  it('updates the confirm password data on input', async () => {
    const mockT = (key) => key;
    const wrapper = mount(SignUp, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
    await wrapper.find('input#floatingCPassword').setValue('Password123');
    expect(wrapper.vm.cpassword).toBe('Password123');
  });
  it('matches passwords correctly', async () => {
    const mockT = (key) => key;
    const wrapper = mount(SignUp, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
    await wrapper.find('input#floatingPassword').setValue('Password123');
    await wrapper.find('input#floatingCPassword').setValue('Password123');
    expect(wrapper.vm.passwordsMatch).toBe(true);
  });

  it('does not match incorrect passwords', async () => {
    const mockT = (key) => key;
    const wrapper = mount(SignUp, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
    await wrapper.find('input#floatingPassword').setValue('Password123');
    await wrapper.find('input#floatingCPassword').setValue('WrongPassword');
    expect(wrapper.vm.passwordsMatch).toBe(false);
  });

  it('enables submit button when not loading', async () => {
    const mockT = (key) => key;
    const wrapper = mount(SignUp, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
    await wrapper.setData({ isLoading: false });
    expect(wrapper.find('#signUp').attributes('disabled')).toBeUndefined();
  });
});
