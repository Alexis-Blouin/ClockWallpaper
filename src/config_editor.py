import configparser
import os


class ConfigEditor:
    config = None

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.edit_config_name = None

    def set_edit_config_name(self, config_name):
        self.edit_config_name = config_name

    def apply_config(self, config_name):
        self.__read_config()
        self.config["DEFAULT"] = {"currentconfig": config_name}
        with open("config/config.ini", "w") as configfile:
            self.config.write(configfile)

    def add_section(
        self,
        config_name,
        images_path,
        fonts_path,
        monitor_id,
        hours,
        minutes,
        split,
    ):
        self.__read_config()
        self.config.add_section(config_name)
        self.config[config_name] = self.__set_param(
            images_path,
            fonts_path,
            monitor_id,
            hours,
            minutes,
            split,
        )
        with open("config/config.ini", "w") as configfile:
            self.config.write(configfile)

    def modify_section(
        self,
        config_name,
        images_path,
        fonts_path,
        monitor_id,
        hours,
        minutes,
        split,
    ):
        self.__read_config()
        if self.edit_config_name == config_name:
            self.config[config_name] = self.__set_param(
                images_path,
                fonts_path,
                monitor_id,
                hours,
                minutes,
                split,
            )
        else:
            self.config.remove_section(self.edit_config_name)
            self.config.add_section(config_name)
            self.config[config_name] = self.__set_param(
                images_path,
                fonts_path,
                monitor_id,
                hours,
                minutes,
                split,
            )
        with open("config/config.ini", "w") as configfile:
            self.config.write(configfile)

    def get_config_name(self):
        self.__read_config()
        return self.config.defaults()["currentconfig"]

    def get_section(self, config_name):
        self.__read_config()
        values = {}
        if self.config.has_section(config_name):
            for key in self.config[config_name]:
                values[key] = self.config[config_name][key]
            return values
        else:
            return values

    def get_section_names(self):
        self.__read_config()
        return self.config.sections()

    def config_name_exist(self, config_name):
        return config_name in self.get_section_names()

    def generate_default_config_name(self):
        section_names = self.get_section_names()
        config_name = "Config_"
        config_id = 1

        while config_name + str(config_id) in section_names:
            config_id += 1
        config_name += str(config_id)

        return config_name

    def __set_param(
        self,
        images_path,
        fonts_path,
        monitor,
        hours,
        minutes,
        split,
    ):
        return {
            "imagepath": images_path,
            "fontpath": fonts_path,
            "monitor": monitor,
            "hours": hours,
            "minutes": minutes,
            "split": split,
        }

    def __read_config(self):
        self.config.read("config/config.ini")
