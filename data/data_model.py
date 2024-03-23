import os
import json

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import matplotlib.pyplot as plt
import pandas as pd

DATA_LABELS = (
    "step_number",
    "state",
    "action_taken",
)

plt.interactive(False)
class DataModel(QObject):

    data_loaded = pyqtSignal(int)
    frame_set = pyqtSignal(int, dict, dict)
    graph_made = pyqtSignal(str)

    own_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()
        self.connect_signals()

        # data vars
        self._loaded_data = None
        self._total_data_frames = 0

        # reward data tracking
        self.reward_data_frame = None
        self.reward_frame_is_dirty = False
        self.reward_data_aggregated = None

        # selected frame vars
        self._current_frame_number = 0
        self._data_labels = None
        self._frame_reward_data = None
        self._data_image_path = None

        # graph settings
        self.graph_dpi = 100
        self.current_graph = None

        self.graph_folder = os.path.join(self.own_dir, "graph_images")
        if not os.path.exists(self.graph_folder):
            os.makedirs(self.graph_folder)

    def connect_signals(self):
        pass

    @pyqtSlot(str)
    def load_data_from_path(self, path_to_load):
        if not os.path.exists(path_to_load):
            print(f"Could not load given path {path_to_load}, as it does not exist")

        with open(path_to_load, "r") as data_file:
            self._loaded_data = json.load(data_file)
        self._total_data_frames = len(self._loaded_data)

        # emit signal back to an ui if we have one
        if self.reward_data_frame:
            self.reward_frame_is_dirty = True
        self.data_loaded.emit(self._total_data_frames)

    def make_reward_data_frame(self):
        if not self.reward_data_frame or self.reward_frame_is_dirty:
            try:
                flat_data = [frame["rewards_given"] for frame in self._loaded_data]
            except KeyError:
                # old pattern delete this
                flat_data = [frame["rewards given"] for frame in self._loaded_data]
            self.reward_data_frame = pd.DataFrame(flat_data)

    @pyqtSlot(int, int, list)
    def make_slider_graph(self, width, height, cols_to_hide):

        self.make_reward_data_frame()

        # we assume a dpi of 100
        width_inches = width / 100
        height_inches = height / 100

        print(f"we have thease cols: {self.reward_data_frame.columns}")
        self.current_graph = self.reward_data_frame[[c for c in self.reward_data_frame.columns if c not in cols_to_hide]].plot(figsize=(width_inches, height_inches),
                                                                                                                               kind="line",
                                                                                                                               grid=True)

        self.current_graph.set_facecolor('gray')  # Set the background color of the plot area
        legend = self.current_graph.get_legend()
        if legend:
            legend.remove()

        plt.tight_layout()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Values are fractions (0 to 1)
        #self.current_graph.axis('off')
        self.current_graph.set_xticks([])
        self.current_graph.set_yticks([])
        self.current_graph.set_xticklabels([])
        self.current_graph.set_yticklabels([])

        self.current_graph.axvline(x=self._current_frame_number, color='red', linestyle='--')

        fig = self.current_graph.figure
        dpi = fig.dpi
        trim_percentage = 0.045  # Desired trim percentage
        fig_width_inch, fig_height_inch = fig.get_size_inches()
        trim_inches = (fig_width_inch * trim_percentage, fig_height_inch * trim_percentage)

        # Calculate new bounding box in inches
        from matplotlib.transforms import Bbox
        new_bbox = Bbox(
            [[trim_inches[0], trim_inches[1]], [fig_width_inch - trim_inches[0], fig_height_inch - trim_inches[1]]])

        # Save the plot
        save_path = os.path.join(self.graph_folder, "graph_slider.png")
        if os.path.exists(save_path):
            os.remove(save_path)
        plt.savefig(save_path, bbox_inches=new_bbox, pad_inches=0, dpi=dpi)
        self.graph_made(save_path)


    @pyqtSlot(int)
    def set_to_frame(self, frame_number):

        self._current_frame_number = frame_number

        frame_index = frame_number-1
        frame_data = self._loaded_data[frame_index]

        print(frame_data)

        self._data_image_path = frame_data.get("vision_image_path")
        self._frame_reward_data = frame_data.get("rewards_given")

        if not self._frame_reward_data:
            self._frame_reward_data = frame_data.get("rewards given")

        data_labels = dict()
        for label in DATA_LABELS:
            data_labels[label] = frame_data[label]
        self._data_labels = data_labels

        self.frame_set.emit(self._current_frame_number,
                            self._frame_reward_data,
                            self._data_labels)

if __name__ == "__main__":
    model = DataModel()
    model.load_data_from_path("E:\Python\Ai_Knight\data\hcure\Mighty_Jungle\Mighty_Jungle_data_list.json")
    model.set_to_frame(1)
    model.make_slider_graph(1370, 120, [])


