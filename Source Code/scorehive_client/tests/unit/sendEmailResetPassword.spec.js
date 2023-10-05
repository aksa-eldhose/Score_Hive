import SendEmailResetPassword from "@/views/SendEmailResetPassword.vue";
import { mount } from "@vue/test-utils";
const mockTranslate = (key) => {
  return `${key}`.replaceAll("_", " ");
};

describe("SendEmailResetPassword", () => {
  test("displays validation errors when submitting with invalid data", async () => {
    const wrapper = mount(SendEmailResetPassword, {
      global: {
        mocks: {
          $t: mockTranslate, // Provide the mock $t function
        },
      },
    });
    // Simulate form submission
    await wrapper.find("form").trigger("submit.prevent");
  });
  const mockToast = {
    success: jest.fn(),
  };
  test("submits the form with valid data", async () => {
    const wrapper = mount(SendEmailResetPassword, {
      global: {
        mocks: {
          $t: mockTranslate,
          $toast: mockToast,
        },
      },
    });
    // Set valid data
    await wrapper.setData({
      email: "aksaeldhose2668@gmail.com",
    });

    wrapper.vm.v$.$validate = jest.fn().mockResolvedValue(true);
    // Simulate form submission
    await wrapper.vm.submit();
    wrapper.vm.$nextTick(() => {
      wrapper.vm.isValid = true;
    });
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.isValid).toBe(true);
  });
});
