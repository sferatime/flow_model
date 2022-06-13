import configparser


class Config:

    data = None
    config_file_name = None

    def __init__(self, config_file_name):
        self.config_file_name = config_file_name
        config = configparser.ConfigParser()
        config.read(self.config_file_name)
        self.data = config
