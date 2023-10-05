import AddMatch from "@/views/AddMatch.vue";
import { shallowMount} from '@vue/test-utils';
describe("AddMatch.vue", () => {
  
    const mockT = (key) => key; 
    const wrapper = shallowMount(AddMatch, {
      global: {
        mocks: {
          $t: mockT,
        },
      },
    });
  it("renders correctly", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("enables submit button when isLoading is false", () => {
    wrapper.setData({ isLoading: false });
    const submitButton = wrapper.find('#submitButton');
    expect(submitButton.attributes("disabled")).toBe("false");
  });

  it("validates if teams A and B are different", async () => {

    // Set the same team for A and B
    wrapper.setData({ teamA: "Team A", teamB: "Team A" });

    await wrapper.vm.$nextTick();

    // Check for the error message
    const errorMessage = wrapper.find("#teamsNotMatch");
    expect(errorMessage.exists()).toBe(true);
    expect(errorMessage.text()).toContain("Team A and Team B cannot be the same");
  });
  it('initially sets "match_type" data property to "0" and checks the "Limited" radio button', () => {

    // Verify that the "match_type" data property is initially set to "0"
    expect(wrapper.vm.match_type).toBe("0");

    // Verify that the "Limited" radio button is checked
    const limitedRadioButton = wrapper.find('input[value="0"]');
    expect(limitedRadioButton.element.checked).toBe(true);

    // Verify that the "Test" radio button is not checked
    const testRadioButton = wrapper.find('input[value="1"]');
    expect(testRadioButton.element.checked).toBe(false);
  });
  it('displays number of overs input field when match_type is "0"', async () => {
    const limitedRadioButton = wrapper.find('input[value="0"]');
    expect(limitedRadioButton.element.checked).toBe(true);
    // Check if the input field for number of overs is visible
    const numberOfOversInput = wrapper.find('input[placeholder="Enter the number of overs"]');
    expect(numberOfOversInput.exists()).toBe(true);
  });
  it('renders the input field', () => {
    const input = wrapper.find('input[type="text"]');
    expect(input.exists()).toBe(true);
  });
});
