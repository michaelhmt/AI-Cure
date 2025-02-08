# python built in
import lzma
import os
import json
from datetime import datetime


# site packages
from PIL import Image

class StepSummary:

    def __init__(self):
        self.step_state = None
        self.step_action = None
        self.step_reward = None
        self.step_vision = None

    # @property
    # def step_vision(self):
    #     return self._step_vision
    #
    # @step_vision.setter
    # def step_vision(self, np_array):
    #     if not isinstance(np_array, np.ndarray):
    #         np_array = np.array([0])
    #     vision_data = {
    #         "shape" : np_array.shape,
    #         "dtype" : str(np_array.dtype),
    #         "image_serialized": msgpack.packb(np_array, default=m.encode)
    #     }
    #     self._step_vision = vision_data
    #
    # @step_vision.getter-
    # def step_vision(self):
    #     image_array = msgpack.unpackb(self._step_vision["image_serialized"], object_hook=m.decode)
    #     return image_array

    def vision_serialized(self):
        return self._step_vision["image_serialized"]

class DataTracker:

    own_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, data_name, run_name):
        # record keeper
        self._step_history = list()
        self.tracker_name = data_name
        self.run_name = run_name
        self.write_number = 1
        self.write_folder = self.get_write_folder()

        self._static_data = dict()

        self._reset()

    def _reset(self):
        # current vars
        self.current_action = None
        self.current_reward = dict()
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

    def add_static_data(self, data_label, data_to_add):
        self._static_data[data_label] = data_to_add

    def write_data(self):
        write_batch_name = f"{self.run_name}_{str(self.write_number).zfill(5)}"
        print(f"Starting data write of {write_batch_name}")
        master_data = list()
        frame_folder = os.path.join(self.write_folder, f"{write_batch_name}_step_frames")
        if not os.path.exists(frame_folder):
            os.makedirs(frame_folder)
        for index, recorded_step in enumerate(self._step_history):  # type: (int, StepSummary)
            step_number = str(index + 1).zfill(10)
            image_save_path = os.path.join(frame_folder, f"{write_batch_name}_step_{step_number}.png")
            frame_image = Image.fromarray(recorded_step.step_vision)
            frame_image.save(image_save_path)
            data = {
                "step_number": step_number,
                "state": recorded_step.step_state,
                "action_taken": recorded_step.step_action,
                "rewards_given": recorded_step.step_reward,
                "vision_image_path": image_save_path
            }
            #print(f"Got data: {data}")
            master_data.append(data)

        # Get the current date and time
        now = datetime.now()

        # Format the date and time
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        meta_data = {
            "write_time": formatted_now,
            "model_run_name": write_batch_name
        }
        meta_data.update(self._static_data)

        master_data.append(meta_data)
        print(f"Have {len(master_data)} steps recorded ")
        write_file_path = os.path.join(self.write_folder, f"{write_batch_name}_data_list.json")
        with open(write_file_path, "w+") as write_file:
            json.dump(master_data, write_file, indent=4)

        self.write_number += 1
        print(f"written data for {self.run_name}")









