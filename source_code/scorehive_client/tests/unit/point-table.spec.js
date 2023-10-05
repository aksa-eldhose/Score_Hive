import { mount } from '@vue/test-utils';
import PointTable from '@/views/PointTable.vue';

describe('PointTable Component', () => {
    it('renders the component', () => {
      const mockRoute = {
        query: {
          tournamentId: 'MzBUb3VybmFtZW50'
        },
       
      };
      const wrapper = mount(PointTable, {
        global: {
          mocks: {
            $route: mockRoute,
          },
        },
      });
  
      expect(wrapper.exists()).toBe(true);
    });
  });