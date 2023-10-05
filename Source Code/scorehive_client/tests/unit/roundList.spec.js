import { shallowMount } from "@vue/test-utils";
import roundList from "@/views/RoundList.vue";
import axios from "axios";

describe("roundList", () => {
  test("renders correctly", () => {
    const wrapper = shallowMount(roundList);
    expect(wrapper.exists()).toBe(true);
  });
  test("fetches roundList on component mount", async () => {
    // Mock the API call using axios
    const mockedList = [
      { id: 1, round: "abc" },
      { id: 1, round: "abc" },
      { id: 1, round: "abc" },
    ];
    jest.spyOn(axios, "get").mockResolvedValue({ data: mockedList });
    
  });
});
