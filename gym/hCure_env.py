# python built in
import subprocess
import time

# project modules
from gym.base_gym import BaseEnv, RewardData
from screen_reader.game_screen_vision.vision_class import GameVisionClass
from config.hcure_config import HcureConfig
import apps.hcure_utils as hcure_utils
import screen_reader.screen_reader_constants as screen_reader_constants

# Site Packages
import psutil

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
        screen_reader_constants.ENEMIES_KILLED_KEY: RewardData(screen_reader_constants.ENEMIES_KILLED_KEY,
                                                               1, -1, reward_difference_mult=1.02),
        screen_reader_constants.TIME_KEY: RewardData(screen_reader_constants.TIME_KEY,
                                                     1, -1000, new_value_pre_processor=time_pre_processor),
        screen_reader_constants.LVL_KEY: RewardData(screen_reader_constants.LVL_KEY,
                                                    1000, -1000)
    }

    state_map = {
        "game_screen": {"restrict_inputs": ["esc", "enter"]},
        "char_select": {"restrict_inputs": ["esc"]}
    }

    @property
    def action_map(self):
        if not bool(self._action_map):
            raw_action_map = dict()
            for index, thease_items in enumerate(self.config.inputs.items()):
                print(f"dict items are: {thease_items}")
                raw_action_map[index] = {"action_name": thease_items[0], "action_key": thease_items[1]}
            self._action_map = raw_action_map
        return self._action_map

    def reset(self, seed=None):
        # vision interface setup
        if self.vision_interface:
            # we assume we have an attached app running so lets kill it
            proc_id = self.vision_interface.proc_id
            process = psutil.Process(proc_id)
            process.terminate()

        new_app = hcure_utils.start_hcure(self.config)
        vision_model_path = self.config.get_vision_model_path()
        self.vision_interface = GameVisionClass(new_app.pid, vision_model_path)

        # reset any vars we track
        self.current_step = 0

        return self.vision_interface.get_window_array(), {}

    def step(self, action):
        reward = 0
        self.vision_interface.find_current_state()
        current_state_name = self.vision_interface.current_state
        state_settings = self.state_map.get(current_state_name)

        key_to_press = self.action_map.get(action)
        can_press_key = True
        if state_settings:
            if key_to_press['action_key'] in state_settings.get('restrict_inputs'):
                can_press_key = False

        # take the action the agent wants
        if can_press_key:
            self.press_key(key_to_press['action_key'])
        self.current_step += 1

        # find what state we are in now
        state_data = self.vision_interface.get_current_state_info()
        current_screen_state = self.vision_interface.get_window_array()
        is_done = self.check_if_done()

        if current_state_name == "char_select" and key_to_press['action_name'] == "proceed":
            # at this point the AI has selected a character so we will just put them in game
            hcure_utils.char_select_to_game()

        # we could not find what sate we are in
        if not state_data:
            return current_screen_state, reward, False, is_done, {}

        for reward_var_name, state_roi_value in state_data.items():
            if reward_var_name in self._reward_table.keys():
                reward_data = self._reward_table[reward_var_name] # type: RewardData
            else:
                continue

            reward_data.set_new_value(state_roi_value)
            roi_reward = reward_data.get_reward_value()
            reward += roi_reward

        return current_screen_state, reward, False, is_done, {}

    def check_if_done(self):
        # maybe check here to see if we are on the game over screen
        if self.current_step >= self.config.get_max_steps():
            return True
        else:
            return False




if __name__ == "__main__":
    yaml_path = "E:\\Python\\Ai_Knight\\config.yaml"
    my_config = HcureConfig(yaml_path)

    my_h_cure_exe_path = "E:\\holocure\\Game_depolyment\\HoloCure.exe"
    vision_model_path = "E:\\Python\\Ai_Knight\\screen_reader\\font_train\\trained_model\\hcure_font_model_5.traineddata"
    proc = subprocess.Popen(my_h_cure_exe_path)
    time.sleep(15)  # allow the proc to start
    proc_id = proc.pid
    vision = GameVisionClass(proc_id, vision_model_path)

    env = HCureEnv(vision, my_config)

    print(env.action_map)