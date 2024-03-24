import sys
import os
from typing import Union

from data.viewer.viewer_base import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, QMimeData
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QCheckBox
class DataViewerUI(Ui_MainWindow):

    """
    UI for loading and display data from the data tracker, requires connection to data model backend
    """

    data_loaded = pyqtSignal(str)
    new_frame_set = pyqtSignal(int)
    slider_changed = pyqtSignal(int, int, list)

    own_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, mainwindow):
        super(DataViewerUI, self).__init__()

        # on the base window
        self.setupUi(mainwindow)

        self.icon_folder = os.path.join(self.own_dir, "icons")
        self.label_widget = list()
        self.feature_reg = dict()

        self.make_frame_viewer()
        self.connect_signals()

    def make_frame_viewer(self):
        self.imge_widget = FrameViewer(self.centralwidget)
        self.imge_widget.setMinimumSize(QtCore.QSize(1296, 759))
        self.imge_widget.setMaximumSize(QtCore.QSize(1296, 759))
        self.imge_widget.setFrameShape(QtWidgets.QFrame.Panel)
        self.imge_widget.setObjectName("imge_widget")
        self.verticalLayout.addWidget(self.imge_widget)

        default_icon = QPixmap(self.get_label_icon("drag_on_drop_prompt_scale"))
        self.imge_widget.setPixmap(default_icon)

    # for resizing the slider
    def resizeEvent(self, event):
        self.update_slider_background()
        super().resizeEvent(event)

    def connect_signals(self):
        self.action_open_data.triggered.connect(self.load_data)
        self.timeline_widget.valueChanged.connect(self.update_slider_background)
        self.imge_widget.load_dropped_data.connect(self.load_data)

        # timeline buttons
        self.btn_step_forward.clicked.connect(lambda: self.timeline_widget.setValue(self.timeline_widget.value() + 1))
        self.btn_step_back.clicked.connect(lambda: self.timeline_widget.setValue(self.timeline_widget.value() - 1))

    def get_enabled_features(self):
        # type: () -> list[str]
        """
        Get a list of feature names that are set to enabled
        """
        enabled_features = list()
        for feature_name, feature_check_box in self.feature_reg.items():
            if feature_check_box.isChecked():
                enabled_features.append(feature_name)
        return enabled_features

    def update_slider_background(self):
        """
        Call to update the slider background, call in the event the current frame is different
        or graph data has been changed/ hidden.
        """
        size = self.timeline_widget.size()  # Get current size of the slider
        self.new_frame_set.emit(self.timeline_widget.value())
        self.slider_changed.emit(size.width(), size.height(), self.get_enabled_features())

    def clear_layout(self, layout):
        # type: (QtWidgets.QLayout) -> None
        """
        Helper method for recursively clearing all children from a layout
        Args:
            layout: the target layout object we want to clear all children from


        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def get_label_icon(self, label_name):
        # type: (str) -> Union[str, None]
        """
        get the icon path for an icon if it's in the icon folder, icon must match label name given exactly.
        Args:
            label_name: The name of label you want the icon for.

        Returns:
            string path to icon if found else returns None

        """
        icon_path = os.path.join(self.icon_folder, f"{label_name}.png")
        if os.path.exists(icon_path):
            return icon_path
        else:
            return None

    def make_and_add_labels(self, data, icon_override=None):
        # type: (dict[str], str) -> None
        """
        Make labels for given data and add to UI label layout.

        Args:
            data: dict of the labels and label values you want to add to the UI
            icon_override: Icon to use instead of searching based on label name

        """
        for label, label_value in data.items():
            # make the widget
            label_widget = ValueWidget(label, self)
            label_widget.set_entry_text(label)
            label_widget.set_label_text(label_value)

            # find icon
            if icon_override:
                label_icon = self.get_label_icon(icon_override)
            else:
                label_icon = self.get_label_icon(label)

            if label_icon:
                label_widget.set_icon(label_icon)

            self.value_widget_holder.addWidget(label_widget)
            self.label_widget.append(label_widget)

    def on_frame_update(self, current_frame_number, reward_data, data_labels, frame_image_path):
        # type: (int, dict[str], dict[str], str) -> None
        """
        Will update UI with new provided frame data

        Args:
            current_frame_number: the frame number we are now set to
            reward_data: data for rewards, key reward name value is reward given for this frame
            data_labels: labels for this frame key is label name and value is label value
            frame_image_path: file path to the image associated with this frame


        """
        self.clear_layout(self.value_widget_holder)

        # make and add new data label
        self.label_widget = list()
        self.make_and_add_labels(data_labels)
        self.make_and_add_labels(reward_data, "reward")

        # space to push them all to the top
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.value_widget_holder.addItem(spacer)

        # set frame
        frame_pixmap = QPixmap(frame_image_path)
        self.imge_widget.setPixmap(frame_pixmap)
        self.imge_widget.resize(frame_pixmap.width(), frame_pixmap.height())

    def on_slider_graph_update(self, new_graph_image_path):
        # type: (str) -> None
        """
        will update the slider with a provided graph image
        Args:
            new_graph_image_path: file path to the new image
        """

        # clear any style sheet settings and make pixmap
        self.timeline_widget.setStyleSheet("QSlider { background-color: none; }")
        pixmap = QPixmap(new_graph_image_path)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))

        # set the image
        self.timeline_widget.setPalette(palette)
        self.timeline_widget.setAutoFillBackground(True)

    def load_data(self, data_path=None):
        """
        Gives the user the chance to browse for a data file
        """
        # Open a file dialog and filter for JSON files
        if not data_path:
            options = QtWidgets.QFileDialog.Options()
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                         "JSON Files (*.json)", options=options)
        else:
            file_path = data_path
        if file_path:
            self.data_loaded.emit(file_path)

    def set_ui_to_data(self, frames, features, data_name):
        """
        On the load of new data will set the UI to the given data

        Args:
            frames: the number of frames in this data used to set timeline slider
            features: the features (cols) found in this data
            data_name: The name of this data to be displayed in the title label
        """

        # set title and slider
        self.timeline_widget.setMaximum(frames)
        self.label_data_title.setText(data_name)

        # add features controls to hide and un-hide features from graph
        layout = self.feature_display.layout()
        self.clear_layout(layout)
        self.feature_reg.clear()
        for feature_name in features:
            feature_checkbox = QCheckBox(feature_name)
            feature_checkbox.setChecked(True)
            feature_checkbox.stateChanged.connect(self.update_slider_background)
            layout.addWidget(feature_checkbox)
            self.feature_reg[feature_name] = feature_checkbox

        self.update_slider_background()
class ValueWidget(QWidget):
    """
    Widget for representing data of a given label
    """

    def __init__(self, label, parent=None):
        super().__init__(parent)
        self.icon_pixmap = None
        self.label = label
        self.widget_set_up()

    def widget_set_up(self):
        # Create the QGroupBox for the value_group_box
        self.value_group_box = QGroupBox(self.label)
        self.value_group_layout = QHBoxLayout()

        # Create the QLabel for the value_icon, value_entry, and value_label
        self.icon = QLabel("icon")
        self.value_entry = QLabel("Entry")
        self.value_label = QLabel("Value")

        # Add the labels to the group box layout
        self.value_group_layout.addWidget(self.icon)
        self.value_group_layout.addWidget(self.value_entry)
        self.value_group_layout.addWidget(self.value_label)

        # Set the layout of the group box
        self.value_group_box.setLayout(self.value_group_layout)

        # The main layout for this widget
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.value_group_box)
        self.setLayout(self.main_layout)

    def set_entry_text(self, text):
        self.value_entry.setText(text)

    def set_label_text(self, text):
        self.value_label.setText(str(text))

    def set_icon(self, image_path):
        self.icon_pixmap = QPixmap(image_path)
        self.icon_pixmap = self.icon_pixmap.scaled(64, Qt.KeepAspectRatio)
        self.icon.setFixedSize(self.icon_pixmap.size())
        self.icon.setPixmap(self.icon_pixmap)

class FrameViewer(QLabel):
    load_dropped_data = pyqtSignal(str)
    def __init__(self, parent=None):
        super(FrameViewer, self).__init__(parent)
        # Enable the widget to accept drops
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        # Check if the event contains a MIME data of the type we accept (here, we accept any)
        if event.mimeData().hasFormat('text/uri-list'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        # Extract the path of the first file from the MIME data
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            file_path = url.toLocalFile()
            if file_path.endswith(".json"):
                print(f"using dropped data: {file_path}")
                self.load_dropped_data.emit(file_path)
                event.accept()
            else:
                print("Data ignored not json")
                event.ignore()
        else:
            event.ignore()

def launch_ui():
    """
    Launch just the UI wil be unconnected to a model
    """
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = DataViewerUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    status = launch_ui()