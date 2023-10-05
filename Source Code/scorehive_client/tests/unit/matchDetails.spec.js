import { mount } from '@vue/test-utils'; 
import MatchDetails from '@/views/MatchDetails.vue'; 

describe('MatchDetails', () => {
  let wrapper; 

  beforeEach(() => {
    wrapper = mount(MatchDetails); // Mount the component before each test
  });

  afterEach(() => {
    wrapper.unmount(); // Unmount the component after each test
  });
  it('renders the component', () => {
    expect(wrapper.exists()).toBe(true);
  });

  it('should initially display card with "Summary" link active', () => {
    const activeLink = wrapper.find('.active-link');

    expect(activeLink.exists()).toBe(true);
    expect(activeLink.text()).toBe('Summary');
  });
  it('should show "Score Card" content when clicking on "Score Card" link', async () => {
    const scoreCardLink = wrapper.find('[data-testid="score-card-link"]');
  
    await scoreCardLink.trigger('click');
  
    await wrapper.vm.$nextTick();
  
    const scoreCardContent = wrapper.find('[data-testid="score-card-content"]');
    expect(scoreCardContent.exists()).toBe(false);
  });
});
