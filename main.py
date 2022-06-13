from App import App
import sys
from Simulation import Simulation


# from Config import Config
# config = Config('./config.toml')

simulation = Simulation()
App = App(simulation, [])
sys.exit(App.exec())
