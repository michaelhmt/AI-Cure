import time

import pymem
# Site package
from pymem import Pymem
from pymem.process import module_from_name
import psutil

from memory_reader.mem_addresses import GameMemoryReadException


class GameMemoryClass:
    def __init__(self, proc_id):
        self.proc_id = proc_id

        self.game_exe = pymem.Pymem()
        self.game_exe.open_process_from_id(proc_id)
        self.game_module = module_from_name(self.game_exe.process_handle, "HoloCure.exe").lpBaseOfDll

        # extra_adresses
        self.extra_adresses = dict()

    def retarget_proc(self, new_proc_id):
        self.proc_id = new_proc_id
        self.game_exe = pymem.Pymem()
        self.game_exe.open_process_from_id(new_proc_id)
        self.game_module = module_from_name(self.game_exe.process_handle, "HoloCure.exe").lpBaseOfDll

    def calculate_address(self, address, offsets):
        mem_adress = self.game_exe.read_longlong(address)
        for cnt, offset in enumerate(offsets):
            if cnt + 1 != len(offsets):
                mem_adress = self.game_exe.read_longlong(mem_adress + offset)
        return mem_adress + offsets[-1]

    def read_pointer(self, pointer_address):
        return self.game_exe.read_double(pointer_address)

    def get_value(self, address_info):
        if address_info.get("is_external"):
            # in this case the value is stored in the extra address's
            retrieval_key = address_info.get("report_key")
            address_value = int(self.extra_adresses.get(retrieval_key, 0), 16)
            try:
                value = self.read_pointer(address_value)
            except:
                return None
            return value
        else:
            address_base = address_info['base']
            address_offsets = address_info['offsets']
            return self.game_exe.read_double(self.calculate_address(self.game_module + address_base, address_offsets))

    def state_is_active(self, state_to_check):
        """
        Loops through the currently loaded states and determines which one if any is currently active.
        """

        test_address, expected_result = state_to_check.state_check()
        try:
            results = self.get_value(test_address)
        except Exception as e:
            print(f"Got error: {e} ")
            return False

        if callable(expected_result):
            in_this_state = expected_result(results)
        else:
            in_this_state = results == expected_result

        return in_this_state

    def get_current_state_info(self, state):
        """
        If a state is currently set will loop through the state rois and report the value of each one.
        """
        state_report = dict()
        for value_name, address_info in state:
            try:
                state_report[value_name] = self.get_value(address_info)
            except pymem.exception.MemoryReadError:
                msg = f"Could not read target address {address_info}"
                print(msg)
                raise GameMemoryReadException(msg)

        return state_report

    def add_app_data(self, app_data):
        # type: (dict) -> None
        self.extra_adresses = app_data


if __name__ == "__main__":
    import apps.hcure_utils as hcure_utils
    import config.hcure_config as hcure_config
    import memory_reader.game_state as mem_states
    import memory_reader.mem_addresses as m_con
    import project_constants

    config_path = project_constants.CONFIG_PATH
    config = hcure_config.HcureConfig(config_path)
    game_proc = hcure_utils.start_hcure(config)
    time.sleep(5)
    mem_interface = GameMemoryClass(game_proc.pid)

    in_game_state = mem_states.MemoryGameState("game", m_con.address, mem_interface)
    time.sleep(20)
    result = mem_interface.state_is_active(in_game_state)
    print(f"are we in game: {result}")
    print(f"are we in game: {result}\n report is {mem_interface.get_current_state_info(in_game_state)}")
