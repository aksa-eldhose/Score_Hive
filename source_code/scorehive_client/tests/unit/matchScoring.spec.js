import { mount } from "@vue/test-utils";
import MatchScoring from "@/views/MatchScoring.vue"; // Make sure to provide the correct path to your component

describe('MatchScoring', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(MatchScoring);
    // Set up necessary data or variables here
    wrapper.vm.batsmen = [
      { name: 'Batsman 1', runs: 0, ballsFaced: 0, teamid: 1, id: 1 },
      { name: 'Batsman 2', runs: 0, ballsFaced: 0, teamid: 1, id: 2 },
    ];
    wrapper.vm.overHistory = [];

    wrapper.vm.playerlist = [
      { player_id: 3, name: 'Batsman 3' },
      { player_id: 4, name: 'Batsman 4' },
    ];
    wrapper.vm.currentBatterIndex = 0;
  });

  it('updates score and over history when updateScore is called with a number', () => {
    // Initial state
    expect(wrapper.vm.batsmen[0].runs).toBe(0);
    expect(wrapper.vm.batsmen[0].ballsFaced).toBe(0);
    expect(wrapper.vm.batsmen[1].runs).toBe(0);
    expect(wrapper.vm.batsmen[1].ballsFaced).toBe(0);
    expect(wrapper.vm.overHistory.length).toBe(0);

    // Call the method with a number
    wrapper.vm.updateScore(4);

    // Assert that the runs and ballsFaced have been updated correctly
    expect(wrapper.vm.batsmen[0].runs).toBe(4);
    expect(wrapper.vm.batsmen[0].ballsFaced).toBe(1);

    // Assert that an entry has been added to overHistory
    expect(wrapper.vm.overHistory.length).toBe(1);
    const overEntry = wrapper.vm.overHistory[0];
    expect(overEntry.value).toBe(4);
    expect(overEntry.runs).toBe(4);
    expect(overEntry.balls).toBe(1);
  });

  it('performs out operation when performOut is called', () => {
    // Initial state
    expect(wrapper.vm.batsmen.length).toBe(2);
    expect(wrapper.vm.overHistory.length).toBe(0);
    expect(wrapper.vm.playerlist.length).toBe(2);

    // Call the method
    wrapper.vm.performOut();

    // Assert that the batsman has been marked as out in overHistory
    expect(wrapper.vm.overHistory.length).toBe(1);
    expect(wrapper.vm.overHistory[0].out).toBe(true);

    // Assert that the playerlist is updated
    expect(wrapper.vm.playerlist.length).toBe(1);

    // Assert that the batsman data is updated as expected
    expect(wrapper.vm.batsmen.length).toBe(2); // Length should remain the same
  });

  it('correctly swaps the currentBatterIndex when swapBatsmen is called', () => {
    // Initial state
    expect(wrapper.vm.currentBatterIndex).toBe(0);

    // Call the method
    wrapper.vm.swapBatsmen();

    // Assert that currentBatterIndex has been updated
    expect(wrapper.vm.currentBatterIndex).toBe(1);

    // Call the method again
    wrapper.vm.swapBatsmen();

    // Assert that currentBatterIndex has been updated again
    expect(wrapper.vm.currentBatterIndex).toBe(0);
  });

  it('handles undoing the last ball when undoLastBall is called', () => {
    // Initial state
    expect(wrapper.vm.batsmen[0].runs).toBe(0);
    expect(wrapper.vm.batsmen[0].ballsFaced).toBe(0);
    expect(wrapper.vm.batsmen[1].runs).toBe(0);
    expect(wrapper.vm.batsmen[1].ballsFaced).toBe(0);
    expect(wrapper.vm.overHistory.length).toBe(0);

    // Update score and over history
    wrapper.vm.updateScore(4);

    // Call the undoLastBall method
    wrapper.vm.undoLastBall();

    // Assert that the runs and ballsFaced have been reset after undoing the last ball
    expect(wrapper.vm.batsmen[0].runs).toBe(0);
    expect(wrapper.vm.batsmen[0].ballsFaced).toBe(0);
    expect(wrapper.vm.overHistory.length).toBe(0); // Over history should be empty after undoing
  });
});
