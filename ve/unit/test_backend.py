'''
Created on Mar 9, 2021

@author: mballance
'''
from tblink.backend import Backend
from tblink.tblink import TbLink


class TestBackend(Backend):
    
    def __init__(self):
        super().__init__()
        self._simtime = 0
        self.timewheel = []
        
    def add_simtime_cb(self, cb, time):
        inserted = False

        # TODO: scale        
        sim_steps = time

        for i in range(len(self.timewheel)):
            if (sim_steps > self.timewheel[i][0]):
                sim_steps -= self.timewheel[i][0]
            elif i+1 < len(self.timewheel) and self.timewheel[i+1][0] > sim_steps:
                offset = self.timewheel[i][0]
                offset -= sim_steps
                self.timewheel[i][0] = offset
                self.timewheel.insert(i, [sim_steps, cb])
                inserted = True
                break

        if not inserted:
            self.timewheel.append([sim_steps, cb])

    def simtime(self)->int:
        return self._simtime
    
    def run(self) -> bool:
        """Spin the timewheel and activate any callbacks"""
        if len(self.timewheel) > 0:
            ev = self.timewheel.pop()
            self._simtime += ev[0]
            ev[1]()
        
        return TbLink.inst().reschedule()
