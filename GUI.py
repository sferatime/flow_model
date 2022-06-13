from PySide6 import QtCore, QtWidgets, QtGui
from GUIFIeld import GUIField
from Config import Config


class GUI(QtWidgets.QWidget):
    layout = None
    field_widget = None
    config = None
    simulation = None

    def __init__(self, config, simulation):
        super().__init__()
        self.config = config
        self.set_layout()
        self.simulation = simulation
        self.init_ui(simulation)

    def set_layout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

    def init_ui(self, simulation):
        self.layout.addWidget(GUIField(
            simulation,
            int(self.config.data["GUI"]["work_field_height"]),
            int(self.config.data["GUI"]["work_field_width"])))
        start_stop_button = QtWidgets.QPushButton("start / stop")
        start_stop_button.clicked.connect(simulation.switch_state)
        self.layout.addWidget(start_stop_button)

