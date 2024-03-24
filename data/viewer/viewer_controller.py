import sys

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets

import data.viewer.viewer as view
import data.data_model as model

# this is more of an interface
class DataController(QObject):
    """
    For connecting up the data view and the data model
    """

    def __init__(self):
        super().__init__()

        self.model = model.DataModel()
        self.view = view.DataViewerUI

        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.view = view.DataViewerUI(self.main_window)
        self.connect_signals()

    def connect_signals(self):

        # view signals
        self.view.data_loaded.connect(self.model.load_data_from_path)
        self.view.new_frame_set.connect(self.model.set_to_frame)
        self.view.slider_changed.connect(self.model.make_slider_graph)

        # model signals
        self.model.data_loaded.connect(self.view.set_ui_to_data)
        self.model.frame_set.connect(self.view.on_frame_update)
        self.model.graph_made.connect(self.view.on_slider_graph_update)

    def launch_ui(self):
        self.main_window.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    ctrl = DataController()
    ctrl.launch_ui()
