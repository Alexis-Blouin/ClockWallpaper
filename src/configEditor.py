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
        )
        with open("../config/config.ini", "w") as configfile:
            self.config.write(configfile)

    def add_user_section(
        self, username, images_path, fonts_path, image_name, font_name, monitor_id
    ):
        self.config.read("config/config.ini")
        self.config.add_section(username)
        self.config[username] = self.__set_param(
            images_path,
            fonts_path,
            image_name,
            font_name,
            monitor_id
        )
        with open("../config/config.ini", "w") as configfile:
            self.config.write(configfile)

    def modify_user_section(
        self, username, images_path, fonts_path, image_name,font_name, monitor_id
    ):
        self.config.read("../config/config.ini")
        self.config[username] = self.__set_param(
            images_path,
            fonts_path,
            image_name,
            font_name,
            monitor_id
        )
        with open("../config/config.ini", "w") as configfile:
            self.config.write(configfile)

    def get_default_section(self):
        self.config.read("../config/config.ini")
        return self.config.defaults()

    def get_user_section(self, username):
        self.config.read("../config/config.ini")
        values = {}
        if username in self.config.sections():
            for key in self.config[username]:
                values[key] = self.config[username][key]
            return values
        else:
            return values

    def __set_param(self, image_path, font_path, image_name, font_name, monitor_id):
        return {
            "imagespath": image_path,
            "fontspath": font_path,
            "fullimagename": image_name,
            "fullfontname": font_name,
            "monitorid": monitor_id,
        }
