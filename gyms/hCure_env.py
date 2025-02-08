# python built in
import subprocess
import time
import traceback

# project modules
import project_constants
from gyms.base_gym import BaseEnv, RewardData
from game_interface.hcure_interface import HcureGameInterface
from config.hcure_config import HcureConfig
import apps.hcure_utils as hcure_utils
import screen_reader.screen_reader_constants as screen_reader_constants
import memory_reader.mem_addresses as mem_constants
from memory_reader.GameMemoryClass import GameMemoryReadException
from data.hcure_data_tracker import HCureDataTracker

# Site Packages
import psutil
import numpy

# constants
REWARD_FOR_INCREASE_KEY = "increased"
REWARD_FOR_DECREASE_KEY = "decreased"


def time_pre_processor(time_str):
    time_int_token = time_str.split(":")
    minutes = time_int_token[0]
    seconds = time_int_token[1]

    pure_seconds_value = (minutes * 60) + seconds
    return pure_seconds_value


class HCureEnv(BaseEnv):
    _action_map = dict()
    _reward_table = {
        mem_constants.KILLS: RewardData(mem_constants.KILLS, 1, -1, reward_difference_mult=1.02),
        mem_constants.LEVEL: RewardData(mem_constants.LEVEL, 1000, -1000),
        mem_constants.EXP: RewardData(mem_constants.EXP, 1.1, -3, reward_difference_mult=1.03),
        mem_constants.COINS: RewardData(mem_constants.COINS, 0.8, -3, reward_difference_mult=1.01),
        mem_constants.HP: RewardData(mem_constants.HP, 0.01, -12, reward_difference_mult=1.2)
    }

    state_map = {
        "game": {"restrict_inputs": ["esc"]},
        "char_select": {"restrict_inputs": ["esc"]},
        "level_up": {"restrict_inputs": ["d"]}
    }
    hold_keys = {"game": ("w", "a", "s", "d")}

    @property
    def action_map(self):
        if not bool(self._action_map):
            raw_action_map = dict()
            for index, thease_items in enumerate(self.config.inputs.items()):
                raw_action_map[index] = {"action_name": thease_items[0], "action_key": thease_items[1]}
            self._action_map = raw_action_map
        return self._action_map

    def reset(self, seed=None):
        # vision interface setup
        if self.game_interface:
            # we assume we have an attached app running so lets end it
            proc_id = self.game_interface.proc_id
            process = psutil.Process(proc_id)
            process.terminate()

        new_app = hcure_utils.start_hcure(self.config)
        self.parent_app.re_target_new_proc(new_app)
        self.game_interface.switch_to_new_game_window(new_app.pid)
        self.data_tracker = HCureDataTracker("hcure", self.model_run_name)

        # reset any vars we track
        self.current_step = 0
        self.total_reward = 0.0

        return self.game_interface.get_window_array(), {}

    def run_step(self, action_to_take, data_tracker):
        reward = 0
        self.game_interface.find_current_state()

        try:
            current_state_name = self.game_interface.current_state.name
        except AttributeError:
            current_state_name = "No state"

        data_tracker.current_state = current_state_name
        print(f"{'=' * 10}\nIn state: {current_state_name}\n {'=' * 10}")
        state_settings = self.state_map.get(current_state_name)

        key_to_press = self.action_map.get(action_to_take)
        can_press_key = True
        if state_settings:
            if key_to_press['action_key'] in state_settings.get('restrict_inputs'):
                print(f"Agent wanted to press {key_to_press['action_key']} is restricted in state {current_state_name}")
                can_press_key = False

        # just encase we are in the level up, but we pressed D as we entered it
        if current_state_name == "level_up":
            self.press_key("esc")

        # take the action the agent wants
        if can_press_key:
            target_key = key_to_press['action_key']
            data_tracker.current_action = target_key
            if current_state_name in self.hold_keys.keys():
                if target_key in self.hold_keys[current_state_name]:
                    self.hold_key(target_key)
                else:
                    self.press_key(target_key)
            else:
                self.press_key(target_key)
        else:
            data_tracker.current_action = f"tried to press {key_to_press['action_key']}"
        self.current_step += 1

        # find what state we are in now
        state_data = self.game_interface.get_current_state_info()
        current_screen_state = self.game_interface.get_window_array()
        is_done = self.check_if_done(state_data)
        data_tracker.current_vision = current_screen_state

        if current_state_name == "char_select" and key_to_press['action_name'] == "proceed":
            # at this point the AI has selected a character so we will just put them in game
            data_tracker.add_static_data("selected_char", state_data.get('selected'))
            hcure_utils.char_select_to_game()
            time.sleep(0.5)
            #  pause the game so we can inject the cheat engine stuff and get a report
            self.press_key("esc")
            self.game_interface.make_cheat_engine_report()
            self.game_interface.focus_game()
            self.press_key("esc")

        # we could not find what sate we are in
        if not state_data:
            return current_screen_state, reward, False, is_done, {}

        reward_data_tracking = dict()
        for reward_var_name, state_roi_value in state_data.items():
            if reward_var_name in self._reward_table.keys():
                reward_data = self._reward_table[reward_var_name]  # type: RewardData
            else:
                continue

            reward_data.set_new_value(state_roi_value)
            roi_reward = reward_data.get_reward_value()
            reward_data_tracking[reward_var_name] = roi_reward
            print(f"reward {reward_var_name} adding {roi_reward} to {reward}")
            reward += roi_reward
            print(f"new reward of {reward}")

        self.total_reward += reward
        reward_data_tracking["cumulative_reward"] = reward
        reward_data_tracking["total_reward"] = float(self.total_reward)
        data_tracker.current_reward = reward_data_tracking

        print(f"Applying reward of: {reward}")

        return current_screen_state, reward, False, is_done, {}

    def step(self, action):
        with self.data_tracker as data_tracker:
            if self.game_interface.is_paused:
                # unpause the game if we are starting a step after data write or learn steps complete
                self.game_interface.pause()
            try:
                step_data = self.run_step(action, data_tracker)
            except (GameMemoryReadException, screen_reader_constants.ScreenReadException) as e:
                print("Failed to read from exe writing data and ending....")
                print(f"error was {e}")
                print(f"Traceback is: {traceback.format_exc()}")
                data_tracker.write_data()
                return numpy.ndarray([]), 0, False, True, {}

            return step_data

    def check_if_done(self, current_sate_report):
        # maybe check here to see if we are on the game over screen
        game_over = False
        if current_sate_report:
            game_over = current_sate_report.get('gameOvered') == 1.0
        if self.current_step >= self.config.get_max_steps() or game_over:
            print(f"Time exceeded or game is over: game over var {game_over}")
            if not game_over:
                # pause the game if we need to
                self.game_interface.pause()
            self.data_tracker.write_data()
            return True
        else:
            return False


if __name__ == "__main__":
    yaml_path = project_constants.CONFIG_PATH
    my_config = HcureConfig(yaml_path)

    my_h_cure_exe_path = project_constants.HCURE_GAME_EXE
    vision_model_path = project_constants.HCURE_OCR_MODEL_PATH
    proc = subprocess.Popen(my_h_cure_exe_path)
    time.sleep(15)  # allow the proc to start
    proc_id = proc.pid
    vision = HcureGameInterface(proc_id, vision_model_path)

    env = HCureEnv(vision, my_config)

    print(env.action_map)
