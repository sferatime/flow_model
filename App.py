from PySide6 import QtWidgets
from GUI import GUI
from Config import Config

CONFIG_FILE_NAME = './config.toml'


class App(QtWidgets.QApplication):
    gui = None
    config = None

    def __init__(self, simulation, argv):

        super().__init__(argv)
        self.init_configuration()
        self.init_gui(simulation)

    def init_configuration(self):
        self.config = Config(CONFIG_FILE_NAME)

    def init_gui(self, simulation):
        self.gui = GUI(self.config, simulation)
        self.gui.resize(int(self.config.data["GUI"]["main_window_height"]),
                        int(self.config.data["GUI"]["main_window_width"]))
        self.gui.show()

