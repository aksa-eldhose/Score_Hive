import updateMatch from "@/views/UpdateMatch.vue";
import { shallowMount} from '@vue/test-utils';
describe("updateMatch.vue", () => {
  
    const mockT = (key) => key; 
    const wrapper = shallowMount(updateMatch, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
  it("renders correctly", () => {
    expect(wrapper.exists()).toBe(true);
  });
});