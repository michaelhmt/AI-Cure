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

    """
    Model for tracking and interacting with data created via the data tracker, emit Qt signals for UI integration
    """

    data_loaded = pyqtSignal(int, list, str)
    frame_set = pyqtSignal(int, dict, dict, str)
    graph_made = pyqtSignal(str)
    next_poi = pyqtSignal(int)

    own_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super().__init__()

        # data vars
        self._loaded_data = None
        self._total_data_frames = 0
        self._metadata = None

        # reward data tracking
        self.reward_data_frame = None # type: pd.DataFrame
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

    @property
    def data_features(self):
        return list(self.reward_data_frame.columns)

    @property
    def data_name(self):
        return self._metadata.get("model_run_name", str())

    @property
    def data_write_time(self):
        return self._metadata.get("write_time", str())

    @pyqtSlot(list, bool)
    def find_next_poi(self, cols_to_search, search_backwards=False):

        print(f"doing poi search with {cols_to_search}, will search backwards? {search_backwards}")
        print(f"searching from: {self._current_frame_number}")
        if search_backwards:
            filtered_data_frame = self.reward_data_frame.loc[self._current_frame_number - 1:, cols_to_search]
            filtered_data_frame = filtered_data_frame.iloc[::-1]
        else:
            filtered_data_frame = self.reward_data_frame.loc[self._current_frame_number + 1:, cols_to_search]

        search_mask = filtered_data_frame.ne(0)
        poi_rows = search_mask.any(axis=1)
        poi_row_indexs = poi_rows[poi_rows].index

        print(f"Got these rows: {poi_rows}")
        print(f"type is {type(poi_rows)}")
        next_poi = poi_row_indexs[0] + 1 if not poi_row_indexs.empty else self._current_frame_number
        self.next_poi.emit(next_poi)

    @pyqtSlot(str)
    def load_data_from_path(self, path_to_load):
        # type: (str) -> None
        """
        Load a json file from a path, json must be a list of dicts ideally made via the data tracker

        Args:
            path_to_load: on disk path to Json file to load

        """
        if not os.path.exists(path_to_load):
            print(f"Could not load given path {path_to_load}, as it does not exist")

        with open(path_to_load, "r") as data_file:
            self._loaded_data = json.load(data_file)

        # extract metadata
        self._metadata = self._loaded_data.pop(-1)
        print(f"I loaded: {len(self._loaded_data)} items")
        self._total_data_frames = len(self._loaded_data)

        # emit signal back to an ui if we have one
        self.make_reward_data_frame()

        self.data_loaded.emit(self._total_data_frames, self.data_features, self.data_name)

    def make_reward_data_frame(self):
        """
        Make Pandas data frame for rewards if one does not exist already
        Returns:

        """
        if self.reward_data_frame is None or self.reward_frame_is_dirty:
            for index, frame in enumerate(self._loaded_data):
                if not frame.get("rewards_given"):
                    frame["rewards_given"] = dict()
                    self._loaded_data[index] = frame

            flat_data = [frame["rewards_given"] for frame in self._loaded_data]
            self.reward_data_frame = pd.DataFrame(flat_data)

    @pyqtSlot(int, int, list)
    def make_slider_graph(self, width, height, cols_to_show):
        # type: (int, int, list[str]) -> None
        """
        main method for making a graph of the rewards data can be set to a custom size and filter the cols

        Args:
            width: width in pixels
            height: height in pixels
            cols_to_show:  list of the cols to display on the graph
        """

        self.make_reward_data_frame()
        # we assume a dpi of 100
        width_inches = width / 100
        height_inches = height / 100
        self.current_graph = self.reward_data_frame[[c for c in self.reward_data_frame.columns if c in cols_to_show]].plot(figsize=(width_inches, height_inches),
                                                                                                                           kind="line",
                                                                                                                           grid=True)

        # remove un wanted graph elements
        self.current_graph.set_facecolor('gray')
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

        # add line that tracks the current frame
        self.current_graph.axvline(x=self._current_frame_number, color='red', linestyle='--')

        # set custom area we want to render so we have no empty white space
        fig = self.current_graph.figure
        dpi = fig.dpi
        trim_percentage = 0.045  # Desired trim percentage
        fig_width_inch, fig_height_inch = fig.get_size_inches()
        trim_inches = (fig_width_inch * trim_percentage, fig_height_inch * trim_percentage)
        from matplotlib.transforms import Bbox
        new_bbox = Bbox(
            [[trim_inches[0], trim_inches[1]], [fig_width_inch - trim_inches[0], fig_height_inch - trim_inches[1]]])

        # Save the plot
        save_path = os.path.join(self.graph_folder, "graph_slider.png")
        if os.path.exists(save_path):
            os.remove(save_path)
        plt.savefig(save_path, bbox_inches=new_bbox, pad_inches=0, dpi=dpi)
        self.graph_made.emit(save_path)

    @pyqtSlot(int)
    def set_to_frame(self, frame_number):
        # type: (int) -> None
        """
        Set the currently selected frame from the existing data
        Args:
            frame_number: frmae number to set to, frame must exist in the data range.
        """
        self._current_frame_number = frame_number

        frame_index = frame_number-1
        frame_data = self._loaded_data[frame_index]

        self._data_image_path = frame_data.get("vision_image_path")
        if not self._data_image_path:
            self._data_image_path = frame_data.get("serlized_vision")

        self._frame_reward_data = frame_data.get("rewards_given")

        if not self._frame_reward_data:
            self._frame_reward_data = frame_data.get("rewards given", {}) or dict()

        print(f"reward data is {self._frame_reward_data}")

        data_labels = dict()
        for label in DATA_LABELS:
            data_labels[label] = frame_data[label]
        self._data_labels = data_labels

        self.frame_set.emit(self._current_frame_number,
                            self._frame_reward_data,
                            self._data_labels,
                            self._data_image_path)

if __name__ == "__main__":
    model = DataModel()
    model.load_data_from_path("E:\Python\Ai_Knight\data\hcure\Mighty_Jungle\Mighty_Jungle_data_list.json")
    model.set_to_frame(1)
    model.make_slider_graph(1370, 120, [])


