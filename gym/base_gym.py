# python built in
import threading
import time

# site packages
from gymnasium import Env, spaces
import pyautogui
import pydirectinput
import numpy as np 

# own modules 
from game_interface.base_game_interface import BaseGameInterface
from config.base_config import BaseConfig

class RewardData:
    def __init__(self, reward_name, increase_reward, decrease_reward,
                 unchanged_reward=None, reward_difference_mult=None, new_value_pre_processor=None):

        self._name = reward_name
        self._increase_amount = increase_reward
        self._decrease_reward = decrease_reward
        self._unchanged_reward = unchanged_reward or 0
        self._difference_mult = reward_difference_mult
        self._current_value = None
        self._val_pre_processor = new_value_pre_processor

        self.reward_history = list()
        self.value_history = list()

    @property
    def name(self):
        return self._name

    def set_new_value(self, new_value):
        if self._val_pre_processor:
            new_value = self._val_pre_processor(new_value)
        else:
            new_value = float(new_value)

        if self._current_value:
            self.value_history.append(self._current_value)

        self._current_value = round(new_value, 4)

    def get_reward_value(self):
        if not self.value_history:
            return 0
        last_value = self.value_history[-1]

        if self._current_value > last_value:
            print(f"increase {self.name} by {self._decrease_reward}")
            reward = self._increase_amount
        elif self._current_value < last_value:
            print(f"decreasing {self.name} by {self._decrease_reward}")
            reward = self._decrease_reward
        else:
            print(f"no change in {self.name} doing {self._unchanged_reward}")
            reward = self._unchanged_reward

        if self._difference_mult:
            reward = reward * ((last_value - self._current_value))

        self.reward_history.append(reward)
        return reward


class BaseEnv(Env):
    
    def __init__(self,
                 game_interface: BaseGameInterface,
                 config: BaseConfig,
                 model_name: str,
                 app):
        super(BaseEnv, self).__init__()

        # set up
        self.game_interface = game_interface
        self.parent_app = app
        self.config = config
        self.current_step = 0

        # actions setup
        self.action_space = spaces.Discrete(len(list(self.action_map.items())))
        self.data_tracker = None

        # observation setup
        window_height, windows_width = self.game_interface.get_window_size()
        self.observation_space = spaces.Box(
            low=0,  # lowest colour value to read
            high=255,  # highest colour value to read
            shape=(window_height, windows_width, 4),
            dtype=np.uint8
        )

        # for data tracking
        self.model_run_name = model_name
        print("env Created")

    @property
    def action_map(self):
        # type: () -> dict
        # redefine in actual env implementation
        return None

    @staticmethod
    def press_key(key_name):
        print(f"Pressing: {key_name}")
        pydirectinput.press(key_name)

    def hold_key(self, key_name, hold_for=1):
        key_thread = threading.Thread(target=self.key_hold, args=(key_name, hold_for))
        key_thread.start()

    def key_hold(self, key_name, hold_for):
        key_pressed = pydirectinput.keyDown(key_name)
        if key_pressed:
            time.sleep(hold_for)
            pydirectinput.keyUp(key_name)


