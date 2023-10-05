import { mount } from "@vue/test-utils";
import PlayerList from "@/views/PlayerList.vue";
import LogoContainer from "@/components/LogoContainer.vue";
import Button from "@/components/Button.vue";
import NavBar from "@/views/NavBar.vue";
import { playerList } from "@/services/playerService";

jest.mock("sweetalert2", () => ({
  fire: jest.fn().mockResolvedValue({ isConfirmed: true }),
}));

jest.mock("@/services/playerService", () => ({
  playerList: jest.fn().mockResolvedValue({
    data: [
      {
        player_id: 1,
        name: "John Doe",
        email: "john@example.com",
      },
      {
        player_id: 2,
        name: "Jane Smith",
        email: "jane@example.com",
      },
    ],
  }),
  removePlayer: jest.fn().mockResolvedValue({}),
}));

describe("PlayerList", () => {
  test("renders the component", () => {
    const wrapper = mount(PlayerList, {
      global: {
        components: {
          LogoContainer,
          Button,
          NavBar,
        },
        mocks: {
          $t: (key) => key,
          $router: {
            push: jest.fn(),
          },
          $route: {
            params: {
              teamId: "VGhpcyBpcyBhIHRlYW1JZGVudGlmaWNhdGlvbg==", // Replace with your base64-encoded teamId
            },
          },
        },
      },
    });

    expect(wrapper.exists()).toBe(true);
  });

  // Add more test cases here as needed...

  // Example test for playerList method
  test("fetches player list on component mount", async () => {
    const wrapper = mount(PlayerList, {
      global: {
        components: {
          LogoContainer,
          Button,
          NavBar,
        },
        mocks: {
          $t: (key) => key,
          $router: {
            push: jest.fn(),
          },
          $route: {
            params: {
              teamId: "VGhpcyBpcyBhIHRlYW1JZGVudGlmaWNhdGlvbg==", // Replace with your base64-encoded teamId
            },
          },
        },
      },
    });

    // Wait for the next tick using await wrapper.vm.$nextTick()
    await wrapper.vm.$nextTick();

    // Assert that the playerList method was called
    expect(playerList).toHaveBeenCalled();

    // Assert that the component's data is correctly set based on the mocked response
    expect(wrapper.vm.cards).toEqual([
      {
        player_id: 1,
        name: "John Doe",
        email: "john@example.com",
      },
      {
        player_id: 2,
        name: "Jane Smith",
        email: "jane@example.com",
      },
    ]);
  });
  test("calls addPlayer and navigates to AddPlayer page", async () => {
    const $router = {
      push: jest.fn(),
    };
    const wrapper = mount(PlayerList, {
      global: {
        components: {
          LogoContainer,
          Button,
          NavBar,
        },
        mocks: {
          $t: (key) => key,
          $router,
          $route: {
            params: {
              teamId: "VGhpcyBpcyBhIHRlYW1JZGVudGlmaWNhdGlvbg==", // Replace with your base64-encoded teamId
            },
          },
        },
      },
    });

    await wrapper.vm.addPlayer();

    expect($router.push).toHaveBeenCalledWith({
      name: "AddPlayer",
      query: {
        team: "VGhpcyBpcyBhIHRlYW1JZGVudGlmaWNhdGlvbg==",
      },
    });
  });
});

