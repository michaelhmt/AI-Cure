import sys


from data.viewer.viewer_base import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class DataViewerUI(Ui_MainWindow):

    data_loaded = pyqtSignal(str)
    new_frame_set = pyqtSignal(int)

    def __init__(self, mainwindow):
        super(DataViewerUI, self).__init__()

        self.setupUi(mainwindow)
        self.connect_signals()

    # for resizing the slider
    def resizeEvent(self, event):
        self.update_slider_background()
        super().resizeEvent(event)

    def connect_signals(self):
        self.action_open_data.triggered.connect(self.load_data)
        #self.

    def update_slider_background(self):
        size = self.timeline_widget.size()  # Get current size of the slider
        self.generateBackground(size.width(), size.height())

    def load_data(self):
        # Open a file dialog and filter for JSON files
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                     "JSON Files (*.json)", options=options)
        if file_path:
            self.data_loaded.emit(file_path)
            print(f"loading  {file_path}")

    def set_ui_to_data(self, frames):
        self.timeline_widget.setMaximum(frames)




def launch_ui():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = DataViewerUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    status = launch_ui()