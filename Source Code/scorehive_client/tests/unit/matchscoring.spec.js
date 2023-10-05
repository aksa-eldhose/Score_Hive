import { mount } from '@vue/test-utils';
import scoring from '@/views/MatchScoring.vue';

describe('scoring Component', () => {
  it('renders the component correctly', () => {
      const wrapper = mount(scoring);
      expect(wrapper.exists()).toBe(true);
    });
    it('does not call any method when validation fails', async () => {
      const wrapper = mount(scoring);
          wrapper.setData({ extraScoreStatus: 'LB' });
          
          wrapper.vm.v$.$validate = jest.fn(() => Promise.resolve(false));
      
          const legByScoreMock = jest.spyOn(wrapper.vm, 'legByScore');
          const wideNoBallScoreMock = jest.spyOn(wrapper.vm, 'wideNoBallScore');
          
          await wrapper.vm.extraScore('4', '1');
      
          expect(legByScoreMock).not.toHaveBeenCalled();
          expect(wideNoBallScoreMock).not.toHaveBeenCalled();
        });
        it('does not call any method when validation fails', async () => {
          const wrapper = mount(scoring);
              wrapper.setData({ extraScoreStatus: 'LB' });
              
              wrapper.vm.v$.$validate = jest.fn(() => Promise.resolve(false));
          
              const legByScoreMock = jest.spyOn(wrapper.vm, 'legByScore');
              const wideNoBallScoreMock = jest.spyOn(wrapper.vm, 'wideNoBallScore');
              
              await wrapper.vm.extraScore('4', '1');
          
              expect(legByScoreMock).not.toHaveBeenCalled();
              expect(wideNoBallScoreMock).not.toHaveBeenCalled();
            });
          
            it('updates data and calls methods when openModal is called', () => {
              const wrapper = mount(scoring);
              const button = 'NB';
              wrapper.vm.openModal(button);
              expect(wrapper.vm.legByFlag).toBe(false);
              expect(wrapper.vm.wideNoBallFlag).toBe(true);
              expect(wrapper.vm.runsByStriker).toBe('');
              expect(wrapper.vm.extras).toBe(1);
              expect(wrapper.vm.extraScoreStatus).toBe('NB');
            });
          
            it('updates data when closeModal is called', () => {
              const wrapper = mount(scoring);
              wrapper.vm.closeModal();
              expect(wrapper.vm.modalOpen).toBe(false);
              expect(wrapper.vm.extras).toBe('');
              expect(wrapper.vm.runsByStriker).toBe('');
              expect(wrapper.vm.extraScoreStatus).toBe('');
            });
      
  });