# project modules
import apps.hcure_utils as hcure_utils
from game_interface.base_game_interface import BaseGameInterface


class HcureGameInterface(BaseGameInterface):

    def add_known_states(self):
        self.clear_states()

        pre_made_states = hcure_utils.make_hcure_states(self.app_instance.memory_class, self.app_instance.vision_class)
        self.add_states(pre_made_states)

    def make_cheat_engine_report(self):
        hcure_utils.clear_files_in_report_folder()
        report = hcure_utils.get_game_state_from_cheat_engine_report(self.proc_id)
        self.app_instance.add_info_mem_interface(report)
