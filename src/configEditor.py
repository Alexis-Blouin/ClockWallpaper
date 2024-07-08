import configparser
import os


class ConfigEditor:
    config = None

    def __init__(self) -> None:
        self.config = configparser.ConfigParser()

        if not os.path.exists("../config/config.ini"):
            self.set_default_section()

    def set_default_section(self):
        username = os.getlogin()
        self.config["DEFAULT"] = self.__set_param(
            f"C:\\Users\\{username}\\Documents\\GitHub\\ClockWallpaper\\Images",
            f"C:\\Users\\{username}\\Documents\\GitHub\\ClockWallpaper\\Fonts",
            "YorMirror.jpg",
            "FiraMono-Regular.ttf",
            "1",
            "200,250,300,180,6,20",
            "400,450,300,232,156,54",
            "400,450,150,180,6,20",
        )
        with open("../config/config.ini", "w") as configfile:
            self.config.write(configfile)

    def add_section(
        self,
        config_name,
        images_path,
        fonts_path,
        image_name,
        font_name,
        monitor_id,
        hours,
        minutes,
        split,
    ):
        self.config.read("config/config.ini")
        self.config.add_section(config_name)
        self.config[config_name] = self.__set_param(
            images_path,
            fonts_path,
            image_name,
            font_name,
            monitor_id,
            hours,
            minutes,
            split,
        )
        with open("../config/config.ini", "w") as configfile:
            self.config.write(configfile)

    def modify_section(
        self,
        config_name,
        images_path,
        fonts_path,
        image_name,
        font_name,
        monitor_id,
        hours,
        minutes,
        split,
    ):
        self.config.read("../config/config.ini")
        self.config[config_name] = self.__set_param(
            images_path,
            fonts_path,
            image_name,
            font_name,
            monitor_id,
            hours,
            minutes,
            split,
        )
        with open("../config/config.ini", "w") as configfile:
            self.config.write(configfile)

    def get_default_section(self):
        self.config.read("../config/config.ini")
        return self.config.defaults()

    def get_section(self, config_name):
        self.__read_config
        values = {}
        if config_name in self.config.sections():
            for key in self.config[config_name]:
                values[key] = self.config[config_name][key]
            return values
        else:
            return values

    def set_config(self, config_name):
        self.__read_config()

    def __set_param(
        self,
        images_path,
        fonts_path,
        image_name,
        font_name,
        monitor_id,
        hours,
        minutes,
        split,
    ):
        return {
            "imagespath": images_path,
            "fontspath": fonts_path,
            "fullimagename": image_name,
            "fullfontname": font_name,
            "monitorid": monitor_id,
            "hours": hours,
            "minutes": minutes,
            "split": split,
        }

    def __read_config(self):
        self.config.read("../config/config.ini")
