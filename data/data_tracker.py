# python built in
import lzma
import os
import json
import msgpack
import msgpack_numpy as m

# site packages
import numpy as np

class StepSummary:

    def __init__(self):
        self.step_state = None
        self.step_action = None
        self.step_reward = None
        self._step_vision = None

    @property
    def step_vision(self):
        return self._step_vision

    @step_vision.setter
    def step_vision(self, np_array):
        if not isinstance(np_array, np.ndarray):
            np_array = np.array([0])
        vision_data = {
            "shape" : np_array.shape,
            "dtype" : str(np_array.dtype),
            "image_serialized": msgpack.packb(np_array, default=m.encode)
        }
        self._step_vision = vision_data

    @step_vision.getter
    def step_vision(self):
        image_array = msgpack.unpackb(self._step_vision["image_serialized"], object_hook=m.decode)
        return image_array

    def vision_serialized(self):
        return self._step_vision["image_serialized"]

class DataTracker:

    own_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, data_name, run_name):
        # record keeper
        self._step_history = list()
        self.tracker_name = data_name
        self.run_name = run_name
        self.write_folder = self.get_write_folder()

        self._reset()

    def _reset(self):
        # current vars
        self.current_action = None
        self.current_reward = None
        self.current_state = None
        self.current_vision = None
        self.current_step = None # type: StepSummary

    def _on_start(self):
        pass

    def _on_exit(self):
        pass

    def __enter__(self):
        self.current_step = StepSummary()
        self._on_start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.current_step.step_action = self.current_action
        self.current_step.step_state = self.current_state
        self.current_step.step_reward = self.current_reward
        self.current_step.step_vision = self.current_vision

        self._on_exit()
        self._step_history.append(self.current_step)
        self._reset()

    def get_write_folder(self):
        write_folder = os.path.join(self.own_dir, self.tracker_name, self.run_name)
        if not os.path.exists(write_folder):
            os.makedirs(write_folder)

        return write_folder

    def write_data(self):

        master_data = list()
        for index, recorded_step in enumerate(self._step_history):  # type: (int, StepSummary)
            step_number = str(index + 1).zfill(10)
            data = {
                "step_number": step_number,
                "state": recorded_step.step_state,
                "action_taken": recorded_step.step_action,
                "rewards given": recorded_step.step_reward,
                "serlized_vision": str(recorded_step.vision_serialized())
            }
            #print(f"Got data: {data}")
            master_data.append(data)

        print(f"Have {len(master_data)} steps recorded ")
        write_file_path = os.path.join(self.write_folder, f"{self.run_name}_data_list.json")
        with open(write_file_path, "w+") as write_file:
            json.dump(master_data, write_file, indent=4)

        print(f"written data for {self.run_name}")









