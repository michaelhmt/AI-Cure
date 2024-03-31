# python built in
import subprocess
import time
import os
import uuid
import pathlib
import datetime

# project modules
from config.base_config import BaseConfig
from gym.base_gym import BaseEnv
from screen_reader.game_screen_vision.vision_class import GameVisionClass
from game_interface.hcure_interface import HcureGameInterface
from memory_reader.GameMemoryClass import GameMemoryClass
from name_gen.run_name_gen import get_random_name

# Site Packages
from stable_baselines3 import A2C, PPO
from stable_baselines3.common import env_checker
from stable_baselines3.common.callbacks import BaseCallback

class GameMonitiorCallBack(BaseCallback):
    def __init__(self, print_freq, pause_step, game_interface, verbose=1):
        super(GameMonitiorCallBack, self).__init__(verbose)
        self.print_freq = print_freq

        self.learning_step_size = pause_step
        self.game_interface = game_interface
        self.pause_called = False

    def _on_step(self) -> bool:
        if self.num_timesteps % self.print_freq == 0:
            print(f"Total timesteps: {self.num_timesteps}")
            if self.pause_called:
                print("un-pauseing game as learning has begun again")
                self.game_interface.pause()
                self.pause_called = False

        if self.num_timesteps % self.learning_step_size == 0:
            print(f"{self.num_timesteps} is a pause step, sending pause command")
            self.game_interface.pause()
            self.pause_called = True

        return True

class BaseApp:
    own_path = pathlib.Path(__file__).parent.resolve()
    own_app_dir = os.path.join(own_path, "test_data")


    def __init__(self, app_name: str, config: BaseConfig, env, check_env=False, app_proc=None):
        # main vars
        self._name = app_name
        self._config = config
        self.env_constructor = env # is the function NOT the instance
        self.check_env = check_env

        # name setting vars
        current_datetime = datetime.datetime.now()
        self.start_time_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        self.model_name = get_random_name()

        # interface object
        self.interface_object = None
        self.target_exe_path = self._config.get_exe_path()
        self.vision_model_path = self._config.get_vision_model_path()
        self.start_up_delay = self._config.get_start_up_time()

        # model saving
        self._model = None
        self.model_out_put_dir = None

        # training settings
        self.run_steps = self._config.get_run_steps()
        self.runs_per_update = self._config.get_runs_per_update()
        self.updates_per_checkpoint = self._config.get_updates_per_checkpoint()
        self.learning_steps = self._config.get_learn_steps()

        self.call_back = None
        self.total_time_steps = 0

        # app settings
        self.app_proc = app_proc
        self.proc_id = None

        # start up functions
        self.activate_interface()
        self.find_save_paths()


        self._env = self.env_constructor(self.interface_object, self.config, self.model_name, self)
        if self.check_env:
            env_checker.check_env(self._env)

    @property
    def name(self):
        return self._name

    @property
    def config(self):
        return self._config

    @property
    def env(self):
        return self._env

    def re_target_new_proc(self, new_proc):
        self.app_proc = new_proc
        self.proc_id = self.app_proc.pid
        self.memory_class.retarget_proc(self.proc_id)

    def activate_interface(self):
        if not self.app_proc:
            self.app_proc = subprocess.Popen(self.target_exe_path)
            time.sleep(self.start_up_delay)

        self.proc_id = self.app_proc.pid

        self.interface_object = HcureGameInterface(self.proc_id, self.config, self)
        self.vision_class = GameVisionClass(self.interface_object.get_window_array, self.vision_model_path)
        self.memory_class = GameMemoryClass(self.proc_id)

        self.interface_object.add_known_states()

    def find_save_paths(self):
        user_set_output_path = self._config.get_output_path()
        if user_set_output_path:
            app_folder_path = user_set_output_path
        else:
            app_folder_path = os.path.join(self.own_app_dir, self.name)

        model_folder_name = f"{self.model_name}_{self.start_time_str}"
        output_dir = os.path.join(app_folder_path, model_folder_name)
        os.makedirs(output_dir)
        self.model_out_put_dir = output_dir

    def add_info_mem_interface(self, info_to_add):
        self.memory_class.add_app_data(info_to_add)

    def run_training(self):
        self.total_time_steps = self.run_steps * self.runs_per_update

        self._model = PPO('CnnPolicy', self.env, verbose=1, n_steps=self.total_time_steps,
                          batch_size=128, n_epochs=3, gamma=0.98)

        self.call_back = GameMonitiorCallBack(print_freq=10, pause_step=self.total_time_steps,
                                              game_interface=self.interface_object, verbose=1)

        for learning_step in range(self.learning_steps):
            total_time_steps = self.run_steps * self.runs_per_update*self.updates_per_checkpoint
            print(f"starting step: {learning_step}")
            print(f"will go to {total_time_steps} and then write checkpoint")
            self._model.learn(total_timesteps=total_time_steps,
                              callback=self.call_back)
            checkpoint_save_path = os.path.join(self.model_out_put_dir, f"{self.model_name}_chkpt_{learning_step}")
            print(f"saving checkpoint to {checkpoint_save_path}")
            self._model.save(checkpoint_save_path)

    def run_testing_interface(self):

        while True:
            current_state = self.interface_object.find_current_state()
            current_state_name = self.interface_object.current_state.name
            state_data = self.interface_object.get_current_state_info()
            print(f"{'='*40}\n\n current state name object is: {current_state}\n"
                  f"current state name is: {current_state_name}\n"
                  f"current state info is: {state_data}")


