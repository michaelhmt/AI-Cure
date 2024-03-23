# project modules
import apps.hcure_utils as hcure_utils
from game_interface.base_game_interface import BaseGameInterface


class HcureGameInterface(BaseGameInterface):

    def add_known_states(self):
        self.clear_states()

        pre_made_states = hcure_utils.make_hcure_states(self._config, self.proc_id, self)
        self.add_states(pre_made_states)
